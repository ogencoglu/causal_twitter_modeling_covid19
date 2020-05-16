'''
inference related modules
'''

from causalnex.inference import InferenceEngine


def marginal_probs(graph, query, observations, verbose=1):
    '''
    [graph]        : causalnex BayesianNetwork object
    [query]        : str
    [observations] : dict
    '''

    ie = InferenceEngine(graph)
    marginals = ie.query(observations)
    marg_probs = marginals[query]

    if verbose:
        print('Marginal probabilities of "{}" | {} = {}'.format(
                                            query, observations, marg_probs))

    return marg_probs
