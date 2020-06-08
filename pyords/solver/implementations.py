"""
pandas-dataframe predicated implementations
building template-based process for input/output
module. 

TODO: abstract in refactor.
"""
from ..cluster.algorithms import DBSCAN # TODO: fix this
from ..distance.matrix import ovrp_haversine_distance_matrix
from .helpers import OrtoolsCvrpDataFrame, ovrp_to_df

import pandas as pd
import numpy as np


def get_ortools_solution(dataframe:pd.DataFrame):
    """
    # scripting out ortools model construction and run
    # df: dataframe input containing every shipment.
      weight,pallets,zipcode,latitude,longitude
      18893,24,46168,39.6893,-86.3919
      19599,25,46168,39.6893,-86.3919
    # distances: distance matrix of all point to point calculations.
    #  [[n0-n0, n0-n1, n0-n2, n0-n3], [...], ...]
    # vehicles: matrix for truck definition.
    #  [[t0_min_weight, t0_max_weight], [...], ...]
    # demand: array of demand (includes origin? TODO: validate).

    TODO: return dataframe with vehicle col
    """
    
    app = OrtoolsCvrpDataFrame(
        dataframe,
        depot_index=0, 
        max_solve_seconds=30
    )
    solution = app.solve()

    return solution