'''
utility functions related to training
'''

from copy import deepcopy

import numpy as np
from causalnex.discretiser import Discretiser

from configs import config as cf


def calculate_splits_chunks(array,
                            n_splits=cf.n_levels,
                            remove_nonzero=True):
    '''
    split a given array to equal sized chunks
    '''

    array = np.sort(array)
    if remove_nonzero:
        array = array[np.nonzero(array)[0]]
    splitted = np.array_split(array, n_splits)

    return [i[-1] for i in splitted][:-1]


def calculate_splits_perc(array,
                          percentiles=cf.percentiles,
                          remove_nonzero=True):
    '''
    split a given array by percentiles
    '''

    array = np.array(array)
    if remove_nonzero:
        array = array[np.nonzero(array)[0]]

    return [np.percentile(array, i) for i in percentiles]


def discretize_df(dataframe):

    fit_feats = deepcopy(dataframe)

    for c_n in cf.numerical_columns:
        splits = calculate_splits_perc(fit_feats[c_n],
                                       percentiles=cf.percentiles)
        fit_feats[c_n] = Discretiser(method='fixed',
                                     numeric_split_points=splits
                                     ).transform(fit_feats[c_n].values)
        if cf.n_levels == 2:
            fit_feats[c_n] = fit_feats[c_n].map(cf.label_dict_two_cat)
        if cf.n_levels == 3:
            fit_feats[c_n] = fit_feats[c_n].map(cf.label_dict_three_cat)
        if cf.n_levels == 4:
            fit_feats[c_n] = fit_feats[c_n].map(cf.label_dict_four_cat)

    for c_s in cf.stat_numerical_columns:
        fit_feats[c_s] = Discretiser(method='fixed',
                                     numeric_split_points=cf.cut_offs[c_s]
                                     ).transform(fit_feats[c_s].values)
        fit_feats[c_s] = fit_feats[c_s].map(cf.label_dict_two_cat)

    fit_feats['sentiment'].loc[fit_feats['sentiment'] < 0] = -1  # neg
    fit_feats['sentiment'].loc[fit_feats['sentiment'] >= 0] = 1  # pos
    fit_feats['sentiment'] = fit_feats['sentiment'].map({-1: 'neg', 1: 'pos'})

    return fit_feats
