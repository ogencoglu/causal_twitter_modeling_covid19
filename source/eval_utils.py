'''
utility functions related to evaluation
'''

import json

from configs import config as cf


def save_logs(countries, metrics, dict_name):
    '''
    [metrics] : list
    [dict_name]  : str
    '''

    logs_dict = {'countries': countries, 'metrics': metrics}
    logs_json = json.dumps(logs_dict)
    f = open('{}/{}.json'.format(cf.LOGS_DIR, dict_name), 'w')
    f.write(logs_json)
    f.close()

    return None


def load_logs(dict_name, return_dict=False):
    '''
    [dict_name]   : str
    [return_dict] : bool
    '''

    with open('{}/{}.json'.format(cf.LOGS_DIR, dict_name)) as logs_json:
        logs = json.load(logs_json)

    if return_dict:
        return logs
    else:
        countries, metrics = logs['countries'], logs['metrics']
        return countries, metrics
