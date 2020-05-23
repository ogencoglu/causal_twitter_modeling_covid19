Implementation of `Causal Modeling of Twitter Activity During COVID-19 <https://arxiv.org/abs/2005.07952>`_ - Gencoglu O. & Gruber M. (2020) 
====================
This repository provides the full implementation. Requires *python 3.7*.

Main Idea
====================
**Distinguishing events that correlate with public attention and sentiment change from events that cause public attention and sentiment change during COVID-19 pandemic**

.. raw:: html

    <img src="https://github.com/ogencoglu/causal_twitter_modeling_covid19/blob/master/media/Twitter_trend.png" height="700px">

Quick Glance at Findings
===================

.. image:: https://github.com/ogencoglu/causal_twitter_modeling_covid19/blob/master/media/causal_graph.png
   :width: 400

Reproduction of Results
====================
1 - Get the data
--------------
See *directory_info* in the *data* directory for the expected files. Template of *tweets.csv* is provided.

2 - Run *causal_inference.ipynb*
-------------------------------
See *source* directory.

Relevant configurations are defined in *configs.py*, e.g.:

  --start_date                       '2020-01-22'
  --end_date                         '2020-03-18'
  --sentiment_model                  'distilbert-base-uncased-finetuned-sst-2-english'
  --percentiles                       [75]
  
*source* directory tree:

.. code-block:: bash

  ├── causal_inference.ipynb
  ├── configs.py
  ├── data_utils.py
  ├── eval_utils.py
  ├── feature_extraction.py
  ├── inference.py
  ├── sentiment.py
  ├── train.py
  └── train_utils.py
  
`Cite <https://scholar.google.com/scholar?q=Causal%20Modeling%20of%20Twitter%20Activity%20During%20COVID-19.%20arXiv%202020>`_
====================

.. code-block::

    @article{gencoglu2020causal,
      title={Causal Modeling of Twitter Activity During COVID-19},
      author={Gencoglu, Oguzhan and Gruber, Mathias},
      journal={arXiv preprint arXiv:2005.07952},
      year={2020}
    }

or

    Gencoglu, Oguzhan, and Gruber, Mathias. "Causal Modeling of Twitter Activity During COVID-19." arXiv preprint arXiv:2005.07952 (2020).
