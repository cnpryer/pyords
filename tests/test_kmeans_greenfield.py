from fyords.cluster import KMeans
import pandas as pd
import numpy as np
from os import path
import logging

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

def test_knownk_kmeans():
    df = pd.read_csv(path.join(this_dir, 'greenfield_testing_data.csv'))
    x = df.latitude.values
    y = df.longitude.values
    k = 3 # three dc solution
    kmeans = KMeans(x, y, k)
    logging.info('kmeans configuration: %s' % kmeans.to_dict())
    assert len(kmeans.centroids) > 0
