from ..pyords.cluster.algorithms import DBSCAN
from ..pyords.cluster.visualizations import BasicDBSCANHelper
from ..pyords.cluster import implementations as imps
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
    previous_shape = df.shape
    df = imps.get_dbscan_clusters(df)

    assert df.shape[0] == previous_shape[0]
    assert df.shape[1] - 1 == previous_shape[1]


if __name__ == '__main__':
    logging.basicConfig(stream=sys.stdout, level=logging.INFO)
    test_basic_dbscan()
    lab.show(block=True)
