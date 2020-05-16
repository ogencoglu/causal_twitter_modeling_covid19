'''
Feature extraction
'''

from copy import deepcopy
import warnings

import numpy as np
import pandas as pd
from tqdm import tqdm

from configs import config as cf


def calculate_change(dataframe_to_be_formatted, clip_min=0):
    '''
    increase
    '''
    dataframe_formatted = deepcopy(dataframe_to_be_formatted)
    for i in range(dataframe_formatted.shape[0]):
        dataframe_formatted.iloc[i, :] = np.diff(
            dataframe_formatted.iloc[i, :], prepend=0
        )

    # clip nonzero values to 0
    if (dataframe_formatted < 0).values.sum():
        warnings.warn('Nonzero change values found!')
    dataframe_formatted = dataframe_formatted.clip(lower=clip_min)

    return dataframe_formatted


def calculate_percentage_change(dataframe_to_be_formatted,
                                fillna=True,
                                smoothing=0.0,
                                clip_min=0,
                                replace_inf=100.0):
    '''
    relative increase
    '''
    dataframe_formatted = deepcopy(dataframe_to_be_formatted)
    for i in range(dataframe_formatted.shape[0]):
        dataframe_formatted.iloc[i, 1:] = np.array((np.diff(
            dataframe_formatted.iloc[i, :], prepend=0
        )[1:] + smoothing) / (dataframe_formatted.iloc[i, 0:-1] + smoothing))

    if fillna:
        dataframe_formatted = dataframe_formatted.fillna(0)

    # clip nonzero values to 0
    if (dataframe_formatted < 0).values.sum():
        warnings.warn('Nonzero percentage change values found!')
    dataframe_formatted = dataframe_formatted.clip(lower=clip_min)

    # clip infinity values to 100
    if (dataframe_formatted == np.inf).values.sum():
        warnings.warn('Infinity percentage change values found!')
    dataframe_formatted = dataframe_formatted.replace([np.inf],
                                                      replace_inf/100.0)

    return dataframe_formatted * 100.0


def days_since_first_case(dataframe_to_be_formatted):
    '''
    days since first official case
    '''
    dataframe_formatted = deepcopy(dataframe_to_be_formatted)
    for index, rows in dataframe_formatted.iterrows():
        first_nonzero = (np.array(rows) != 0).argmax(axis=0)
        dataframe_formatted.loc[index] = [0] * first_nonzero + list(
            range(len(rows)-first_nonzero)
        )

    return dataframe_formatted


def is_first_occurance(dataframe_to_be_formatted):
    '''
    day of first infection
    '''
    dataframe_formatted = deepcopy(dataframe_to_be_formatted)
    for index, rows in dataframe_formatted.iterrows():
        first_nonzero = (np.array(rows) != 0).argmax(axis=0)
        dataframe_formatted.loc[index] = 0
        dataframe_formatted.loc[index].iloc[first_nonzero] = 1
        if dataframe_to_be_formatted.loc[index][0] == 0:
            dataframe_formatted.loc[index][0] = 0

    return dataframe_formatted


def is_infected(dataframe_to_be_formatted):
    '''
    1 if the country has at least 1 confirmed case
    '''

    return (dataframe_to_be_formatted > 0.5).astype(int)


def gov_announcement(dataframe_to_be_formatted, country, left_and_right=1):
    '''
    government restriction / lockdown announcement
    '''

    dataframe_formatted = deepcopy(dataframe_to_be_formatted)
    dataframe_formatted = dataframe_formatted.replace(dataframe_formatted, 0)
    if country not in cf.restrictions.keys():
        return dataframe_formatted
    col_ind = np.where(
                dataframe_formatted.columns == cf.restrictions[country])[0]
    if col_ind.shape[0] == 0:
        return dataframe_formatted
    dataframe_formatted.loc[country][
                col_ind[0]-left_and_right:col_ind[0]+left_and_right + 1] = 1

    return dataframe_formatted


def get_feature_matrix(country_counts, covid, mode, country_list):
    '''
    [mode] : 'infected' or 'deaths'
    '''
    all_merged = []
    for country in tqdm(country_list):
        merged = pd.merge(
            pd.DataFrame(data=covid.T[country]),
            country_counts[country_counts['Location'] == country],
            how='outer',
            left_index=True,
            right_on='date'
        )
        merged.drop(['Location'], axis=1, inplace=True)
        merged.fillna(value=0, inplace=True)
        merged.rename(columns={country: mode}, inplace=True)
        merged.reset_index(drop=True, inplace=True)

        # add change
        merged = pd.merge(
            merged,
            pd.DataFrame(data=calculate_change(covid).T[country]),
            how='outer',
            right_index=True,
            left_on='date'
        )
        merged.rename(columns={country: '{}_new'.format(mode)}, inplace=True)

        # add percentage change
        merged = pd.merge(
            merged,
            pd.DataFrame(data=calculate_percentage_change(covid).T[country]),
            how='outer',
            right_index=True,
            left_on='date'
        )
        merged.rename(columns={country: '{}_perc_change'.format(mode)},
                      inplace=True)

        # add government restriction
        merged = pd.merge(
            merged,
            pd.DataFrame(data=gov_announcement(covid, country).T[country]),
            how='outer',
            right_index=True,
            left_on='date'
        )
        merged.rename(columns={country: 'restriction'},
                      inplace=True)

        # add country stats
        merged['over_65'] = cf.over_65[country]
        merged['twitter_usage'] = cf.twitter_usage[country]
        merged['single_household'] = cf.single_household[country]

        # normalize
        for c in ['twitter_activity', mode, '{}_new'.format(mode)]:
            merged[c] = merged[c] / cf.population[country]

        merged.sort_values(by=['date'], inplace=True)
        all_merged.append(merged)

    return pd.concat(all_merged)
