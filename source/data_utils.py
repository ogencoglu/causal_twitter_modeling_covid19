'''
utility functions related to data
'''

import numpy as np
import pandas as pd

import reverse_geocoder as rg

from configs import config as cf


def reformat_date(date_to_be_formatted):
    '''transform column to YYYY-MM-DD'''

    date_split = date_to_be_formatted.split('/')
    date_padded_split = [str(item).zfill(2) for item in date_split]
    date_formatted = '20{}-{}-{}'.format(date_padded_split[2],
                                         date_padded_split[0],
                                         date_padded_split[1])

    return(date_formatted)


def reformat_dataframe(dataframe_to_be_formatted):
    '''
    Groupby (sum) Country & drop 'Province/State', 'Lat', 'Long'
    '''

    # shorten colum name
    dataframe_to_be_formatted = dataframe_to_be_formatted.rename(
        columns={'Country/Region': 'Country'},  inplace=False
    )

    # drop some columns
    dataframe_to_be_formatted = dataframe_to_be_formatted.drop(
        columns=['Province/State', 'Lat', 'Long'], axis=0, inplace=False
    )
    dataframe_formatted = dataframe_to_be_formatted.groupby(['Country']).sum()

    # change column name format
    for column in dataframe_formatted:
        dataframe_formatted = dataframe_formatted.rename(
            columns={column: reformat_date(column)}
        )

    # rolling window of 2
    dataframe_formatted = dataframe_formatted.rolling(
                                                      window=3,
                                                      win_type=None,
                                                      axis=1
                                                      ).mean().round(
                                                      ).fillna(
                                                      value=0
                                                      ).astype(int)

    # filter with dates
    dataframe_formatted = dataframe_formatted.iloc[
                            :, dataframe_formatted.columns <= cf.end_date]
    dataframe_formatted = dataframe_formatted.iloc[
                            :, dataframe_formatted.columns >= cf.start_date]

    return(dataframe_formatted)


def read_covid(data_path, columns='all'):
    '''
    read official covid data
    '''
    if columns == 'all':
        covid = pd.read_csv(data_path)
    else:
        covid = pd.read_csv(data_path, usecols=columns)
    # remove incorrect entry of lat and long zeros
    covid = covid[~np.logical_and(covid.Long == 0, covid.Long == 0)]

    return covid


def read_tweets(tweets_path):
    '''
    read tweets data
    '''

    tweets = pd.read_csv(tweets_path)
    tweets.drop_duplicates(inplace=True, subset='id')

    # shorten date and filter with date limits (see configs)
    tweets['date'] = tweets['date'].str[0:10]
    tweets = tweets[tweets['date'] >= cf.start_date]
    tweets = tweets[tweets['date'] <= cf.end_date]

    # format some columns
    tweets.rename(columns=cf.tweet_column_shortener_dict, inplace=True)
    tweets[['Lat', 'Long']] = np.round(tweets[['Lat', 'Long']], 4)

    # create a new string column called 'Lat_Long' (below is faster than apply)
    tweets['Lat_Long'] = tweets.Lat.astype(str).str.cat(
                                            tweets.Long.astype(str), sep='_')

    # add country to tweets data by latitude and longtitude mapping
    infected = pd.read_csv(cf.INFECTED_PATH,
                           usecols=['Lat', 'Long', 'Country/Region'])

    # format some columns
    infected.rename(columns={'Country/Region': 'Location'}, inplace=True)
    infected[['Lat', 'Long']] = np.round(infected[['Lat', 'Long']], 4)

    # create a new string column called 'Lat_Long'
    infected['Lat_Long'] = infected.Lat.astype(str).str.cat(
                                        infected.Long.astype(str), sep='_')
    infected.drop(['Lat', 'Long'], axis=1, inplace=True)

    # map location from Lat and Long
    tweets['Location'] = tweets['Lat_Long'].map(dict(zip(infected['Lat_Long'],
                                                infected['Location'])))

    print('Tweets dataframe shape={}'.format(tweets.shape))
    return tweets


def add_missing_countries(tweets_df):
    '''
    Note: this functions work 'inplace'
    '''

    print('{} tweets do not have country information!'.format(
                                        tweets_df['Location'].isna().sum()))

    # get tweets without a country info
    no_country = tweets_df[tweets_df['Location'].isna()][
                                            ['Lat', 'Long']].drop_duplicates()

    # extract coordinates
    coordinates = list(no_country.itertuples(index=False, name=None))

    # map coordinates with countries using an external package
    results = rg.search(coordinates)
    no_country['found_countries'] = [i['cc'] for i in results]
    no_country['found_countries'] = no_country[
                        'found_countries'].map(cf.country_abbr)
    no_country['Lat_Long'] = no_country[['Lat', 'Long']].apply(
                                        lambda x: '_'.join(x.map(str)), axis=1)

    # add mapped countries to the original tweets data
    tweets_df.loc[tweets_df['Location'].isna(), 'Location'] = list(tweets_df[
                            tweets_df['Location'].isna()]['Lat_Long'
                                                          ].map(
                    dict(zip(
                          no_country['Lat_Long'], no_country['found_countries']
                                                    ))))
    tweets_df.drop(['Lat_Long'], axis=1, inplace=True)

    print('{} tweets that do not have country information will be discarded!'
          .format(tweets_df['Location'].isna().sum()))
    tweets_df = tweets_df[~tweets_df['Location'].isna()]

    return None
