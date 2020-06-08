from ..pyords.solver import implementations as imps
import logging
from os import path
import pandas as pd

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

def test_basic_cvrp():
    df = pd.read_csv(path.join(this_dir, 'vrp_testing_data.csv'))
    previous_shape = df.shape
    df = imps.get_ortools_solution_dataframe(df)

    # TODO: update for pandas output implementation update
    assert df.shape[0] == previous_shape[0] # TODO: update for solution refactor