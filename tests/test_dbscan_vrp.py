from fyords.cluster import DBSCAN
import pandas as pd
import numpy as np
from os import path
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

    dbscan = DBSCAN(epsilon, minpts)
    dbscan.fit(x, y)
    dbscan.predict()
    logging.info('dbscan configuration: %s' % dbscan.to_dict())
    assert len(dbscan.X) == len(dbscan.clusters)
