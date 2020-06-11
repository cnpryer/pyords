from ..pyords.solver.implementations import (
    get_ortools_solution_dataframe,
    get_many_ortools_solutions_dataframe
)
from ..pyords.cluster.implementations import get_dbscan_clusters
import logging
from os import path
import pandas as pd

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

def test_basic_cvrp():
    df = pd.read_csv(path.join(this_dir, 'vrp_testing_data.csv'))
    previous_shape = df.shape
    df = get_ortools_solution_dataframe(df)

    # TODO: update for pandas output implementation update
    assert df.shape[0] == previous_shape[0] # TODO: update for solution refactor

def test_dbscan_cvrp():
    df = pd.read_csv(path.join(this_dir, 'vrp_testing_data.csv'))[:20]
    previous_shape = df.shape
    df = get_dbscan_clusters(df)
    df = get_many_ortools_solutions_dataframe(df, segmentation_col='cluster')

    # TODO: update for pandas output implementation update
    assert df.shape[0] == previous_shape[0] # TODO: update for solution refactor
    
    assert df.vehicle.nunique() < len(df) # assumed optimizing for aggregation