'''
configs & settings are defined in this file
'''


from os.path import join
from os.path import abspath
from os.path import dirname
from os import pardir
from datetime import datetime

import numpy as np


class Config(object):

    # directory paths
    CURRENT_DIR = abspath(dirname(__file__))
    ROOT_DIR = abspath(join(CURRENT_DIR, pardir))
    DATA_DIR = abspath(join(ROOT_DIR, 'data'))
    LOGS_DIR = abspath(join(ROOT_DIR, 'logs'))

    # data file paths
    TWEETS_PATH = abspath(join(DATA_DIR, 'tweets.csv'))
    INFECTED_PATH = abspath(join(DATA_DIR,
                            'time_series_covid19_confirmed_global.csv'))
    DEATHS_PATH = abspath(join(DATA_DIR,
                          'time_series_covid19_deaths_global.csv'))

    # time window of the analysis
    start_date = '2020-01-22'  # inclusive
    end_date = '2020-03-18'  # inclusive
    date_diff = datetime.strptime(
            end_date, '%Y-%m-%d') - datetime.strptime(start_date, '%Y-%m-%d')
    n_days = date_diff.days + 1

    tweet_column_shortener_dict = {
                                'lat': 'Lat',
                                'long': 'Long',
                                'Country/Region': 'Location'
                                }

    countries = ['Italy', 'Spain', 'Germany', 'France', 'Switzerland',
                 'United Kingdom', 'Netherlands', 'Norway', 'Austria',
                 'Belgium', 'Sweden', 'Denmark']

    n_countries = len(countries)

    # sentiment detection
    sentiment_tokenizer_model = 'distilbert-base-uncased'
    sentiment_model = 'distilbert-base-uncased-finetuned-sst-2-english'

    # country stats
    population = {
                    'Austria': 8.955,
                    'Belgium': 11.539,
                    'Czechia': 10.689,
                    'Denmark': 5.772,
                    'Finland': 5.532,
                    'France': 65.130,
                    'Germany': 83.517,
                    'Greece': 10.473,
                    'Italy': 60.550,
                    'Netherlands': 17.097,
                    'Norway': 5.379,
                    'Portugal': 10.226,
                    'Spain': 46.737,
                    'Sweden': 10.036,
                    'Switzerland': 8.591,
                    'United Kingdom': 67.530,
    }  # pop/km2 - source: wikipedia
    # https://en.wikipedia.org/wiki/List_of_countries_by_population_(United_Nations)
    population_cutoffs = [np.median([i[1] for i in population.items()])]

    over_65 = {
                    'Austria': 19.002,
                    'Belgium': 18.789,
                    'Czechia': 19.421,
                    'Denmark': 19.813,
                    'Finland': 21.721,
                    'France': 20.035,
                    'Germany': 21.462,
                    'Greece': 21.655,
                    'Italy': 22.752,
                    'Netherlands': 19.196,
                    'Norway': 17.049,
                    'Portugal': 21.954,
                    'Spain': 19.379,
                    'Sweden': 20.096,
                    'Switzerland': 18.623,
                    'United Kingdom': 18.396,
    }  # percentage
    # https://data.worldbank.org/indicator/sp.pop.65up.to.zs?end=2018&start=1960
    over_65_cutoffs = [np.median([i[1] for i in over_65.items()])]

    twitter_usage = {
                'Austria': 7.2,
                'Belgium': 8.7,
                'Czechia': 17.2,
                'Denmark': 10.7,
                'Finland': 16.7,
                'France': 10.5,
                'Germany': 9.8,
                'Greece': 2.12,
                'Italy': 7.7,
                'Netherlands': 10.6,
                'Norway': 14.6,
                'Portugal': 5.35,
                'Spain': 4.6,
                'Sweden': 9.6,
                'Switzerland': 12.0,
                'United Kingdom': 37.1,
    }  # % people in February 2020 - source:
# https://gs.statcounter.com/social-media-stats/all/united-kingdom
    twitter_usage_cutoffs = [np.median([i[1] for i in twitter_usage.items()])]

    single_household = {
                'Austria': 37.2,
                'Belgium': 35.0,
                'Czechia': 28.7,
                'Denmark': 43.9,
                'Finland': 44.7,
                'France': 36.2,
                'Germany': 41.7,
                'Greece': 25.7,
                'Italy': 32.6,
                'Netherlands': 38.3,
                'Norway': 45.8,
                'Portugal': 23.1,
                'Spain': 25.5,
                'Sweden': 42.5,
                'Switzerland': 38.1,
                'United Kingdom': 30.5,
    }  # % single person households - source:
# https://appsso.eurostat.ec.europa.eu/nui/show.do?dataset=ilc_lvph02&lang=en
    single_household_cutoffs = [
                        np.median([i[1] for i in single_household.items()])]

    cut_offs = {
                'twitter_usage': twitter_usage_cutoffs,
                'over_65': over_65_cutoffs,
                'single_household': single_household_cutoffs
    }

    country_abbr = {
                    'CN': 'Mainland China',
                    'US': 'US',
                    'GB': 'United Kingdom',
                    'FR': 'France',
                    'PS': 'Palestine',
                    'CA': 'Canada',
                    'GH': 'Ghana',
                    'GU': 'Guam',
                    'GY': 'Guyana',
                    'GP': 'Guadeloupe',
                    'AG': 'Guadeloupe',
                    'LC': 'Saint Lucia',
                    'BJ': 'Benin',
                    'AU': 'Australia',
                    'VI': 'Virgin Islands',
                    'ZM': 'Zambia',
                    'TT': 'Trinidad and Tobago',
                    'KE': 'Kenya',
                    'CO': 'Colombia',
                    'PR': 'Puerto Rico',
                    'ET': 'Ethiopia',
                    'SO': 'Somalia',
                    'BS': 'Bahamas',
                    'NA': 'Namibia',
                    'KY': 'Cayman Islands',
                    'SZ': 'Swaziland',
                    'ME': 'Montenegro',
                    'CU': 'Cuba',
                    'UY': 'Uruguay',
                    'CW': 'Curacao',
                    'GT': 'Guatemala',
                    'XK': 'Kosovo',
                    'SD': 'Sudan',
                    'LR': 'Liberia',
    }

    restrictions = {
                    'Austria': '2020-03-16',
                    'Belgium': '2020-03-18',
                    'Czechia': '2020-03-16',
                    'Denmark': '2020-03-11',
                    'Finland': '2020-03-27',
                    'France': '2020-03-17',
                    'Germany': '2020-03-20',
                    'Greece': '2020-03-23',
                    'Italy': '2020-03-09',
                    'Netherlands': '2020-03-16',
                    'Norway': '2020-03-12',
                    'Portugal': '2020-03-19',
                    'Spain': '2020-03-14',
                    'United Kingdom': '2020-03-24',
    }
    # source :
    # https://en.wikipedia.org/wiki
    #           /National_responses_to_the_2019%E2%80%9320_coronavirus_pandemic

    # training related
    n_observations = n_days * n_countries
    splits = np.array(np.array_split(np.arange(n_observations), n_countries))

    # discrete labels
    percentiles = [75]
    n_levels = len(percentiles) + 1
    label_dict_two_cat = {0: 'low', 1: 'high'}

    numerical_columns = ['infected', 'infected_new', 'infected_perc_change',
                         'deaths', 'deaths_new', 'deaths_perc_change',
                         'twitter_activity']

    stat_numerical_columns = [
                              'over_65',
                              'twitter_usage',
                              'single_household'
                             ]

    tabu_child_nodes = stat_numerical_columns + ['restriction']
    tabu_parent_nodes = ['twitter_activity', 'sentiment']
    tabu_edges = [
                     ('twitter_usage', 'infected'),
                     ('twitter_usage', 'infected_new'),
                     ('twitter_usage', 'infected_perc_change'),
                     ('twitter_usage', 'deaths'),
                     ('twitter_usage', 'deaths_new'),
                     ('twitter_usage', 'deaths_perc_change'),

                     ('restriction', 'infected'),
                     ('restriction', 'infected_new'),
                     ('restriction', 'infected_perc_change'),
                     ('restriction', 'deaths'),
                     ('restriction', 'deaths_new'),
                     ('restriction', 'deaths_perc_change'),

                     ('over_65', 'twitter_activity'),
                     ('over_65', 'sentiment'),
                     ('single_household', 'twitter_activity'),
                     ('single_household', 'sentiment'),
                     ('twitter_usage', 'sentiment'),
                    ]

    edge_threshold = 0.3


config = Config()
