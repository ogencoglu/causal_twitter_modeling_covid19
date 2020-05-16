'''
laguage & sentiment detection
'''

from copy import deepcopy
import numpy as np
from pandarallel import pandarallel
from langdetect import detect
from tqdm import tqdm
from transformers import (pipeline, AutoModelForSequenceClassification,
                          AutoTokenizer)

from configs import config as cf


def detect_lang(text):
    '''
    return language of the text
    '''
    try:
        return detect(text)
    except:
        return 'no_lang'


def add_lang(dataframe):
    '''
    add language as a new column
    [dataframe] : pandas dataframe
    '''
    df_copy = deepcopy(dataframe)
    pandarallel.initialize(progress_bar=True)
    df_copy['lang'] = df_copy['text'].parallel_apply(detect_lang)

    return df_copy


def add_sentiment(dataframe):
    '''
    add sentiment score as a new column, range=[-100,100]
    [dataframe] : pandas dataframe
    '''
    df_copy = deepcopy(dataframe)

    tokenizer = AutoTokenizer.from_pretrained(
                    pretrained_model_name_or_path=cf.sentiment_tokenizer_model)
    model = AutoModelForSequenceClassification.from_pretrained(
                              pretrained_model_name_or_path=cf.sentiment_model)
    sentiment_analyzer = pipeline('sentiment-analysis',
                                  framework='pt',
                                  model=model,
                                  tokenizer=tokenizer,
                                  device=0)

    df_copy['sentiment'] = np.nan
    for row in tqdm(range(df_copy.shape[0])):
        if df_copy['lang'].iloc[row] == 'en':
            sentiment = sentiment_analyzer(df_copy['text'].iloc[row])
            score = sentiment[0]['score']
            label = sentiment[0]['label']
            if label == 'POSITIVE':
                df_copy['sentiment'].iloc[row] = 100 * score
            elif label == 'NEGATIVE':
                df_copy['sentiment'].iloc[row] = -100 * score
            else:
                raise ValueError
        else:
            continue

    return df_copy
