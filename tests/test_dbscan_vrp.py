from fyords.cluster import DBSCAN
import pandas as pd
import numpy as np
from os import path

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

def test_basic_dbscan():
    df = pd.read_csv(path.join(this_dir, 'vrp_testing_data.csv'))
    assert not df.empty
