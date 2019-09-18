from fyords.cluster import KMeans
import pandas as pd
import numpy as np
from os import path
import logging

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

def test_knownk_kmeans():
    df = pd.read_csv(path.join(this_dir, 'greenfield_testing_data.csv'))

    # simplify euclidean distance calculation by projecting to positive vals
    x = df.latitude.values + 90
    y = df.longitude.values + 180

    k = 2 # desired n locations solution
    kmeans = KMeans(k)
    logging.info('kmeans configuration: %s' % kmeans.to_dict())

    kmeans.fit(x, y)
    kmeans.predict()
    logging.info('result: %s' % kmeans.centroids)
    assert len(kmeans.centroids) == k
