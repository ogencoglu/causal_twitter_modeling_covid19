'''
training related functions
'''

from causalnex.network import BayesianNetwork


def train_bn(data, graph):

    bn = BayesianNetwork(graph)
    bn = bn.fit_node_states(data)
    bn = bn.fit_cpds(data, method='BayesianEstimator', bayes_prior='K2')

    return bn
