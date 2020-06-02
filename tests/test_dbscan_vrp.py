from ..pyords.cluster import DBSCAN
from ..pyords.cluster.visualizations import BasicDBSCANHelper
import matplotlib.pylab as lab
import pandas as pd
import numpy as np
from os import path
import sys
import logging

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

def test_basic_dbscan():
    df = pd.read_csv(path.join(this_dir, 'vrp_testing_data.csv'))
    epsilon = 0.79585 # approximate degree delta for 50 miles
    minpts = 2 # at least cluster 2

    # simplify euclidean distance calculation by projecting to positive vals
    x = df.latitude.values + 90
    y = df.longitude.values + 180

    lab.close('all')
    viz = BasicDBSCANHelper()

    dbscan = DBSCAN(epsilon, minpts, viz=viz)
    dbscan.fit(x, y)
    dbscan.predict()
    dbscan.viz.update(dbscan.clusters)

    logging.info('dbscan configuration: %s' % dbscan.to_dict())
    logging.info('dbscan unique result: %s' % set(dbscan.clusters))
    assert len(dbscan.X) == len(dbscan.clusters)

if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    test_basic_dbscan()
    lab.show(block=True)
