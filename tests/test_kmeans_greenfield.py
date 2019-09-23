from fyords.cluster import KMeans
from fyords.cluster.visualizations import BasicAlgoHelper
import matplotlib.pylab as lab
import pandas as pd
import numpy as np
from os import path, system
import logging

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

def test_knownk_kmeans(kopen=False):
    df = pd.read_csv(path.join(this_dir, 'greenfield_testing_data.csv'))

    # simplify euclidean distance calculation by projecting to positive vals
    x = df.latitude.values + 90
    y = df.longitude.values + 180

    viz = BasicAlgoHelper()

    k = 2 # desired n locations solution
    kmeans = KMeans(k, viz)
    logging.info('kmeans configuration: %s' % kmeans.to_dict())

    kmeans.fit(x, y)
    kmeans.predict()
    x2 = [c[0] for c in kmeans.centroids]
    y2 = [c[1] for c in kmeans.centroids]
    kmeans.viz.update(x2, y2)
    logging.info('result: %s' % kmeans.centroids)
    assert len(kmeans.centroids) == k

if __name__ == '__main__':
    test_knownk_kmeans()
    lab.show(block=True)
