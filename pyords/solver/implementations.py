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


def get_ortools_solution_dataframe(dataframe:pd.DataFrame):
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
    dataframe = dataframe.reset_index(drop=True)
    app = OrtoolsCvrpDataFrame(
        dataframe.copy(),
        depot_index=0, 
        max_solve_seconds=30
    )
    app.solve()    

    return app.df

def get_many_ortools_solutions_dataframe(dataframe:pd.DataFrame, segmentation_col:str):
    result = pd.DataFrame(columns=dataframe.columns.tolist()+['vehicle'])
    
    # TODO: create concurrent tasks for segment optimizations
    for segment in dataframe[segmentation_col].unique():
        segdf = dataframe[dataframe[segmentation_col] == segment].copy()
        
        if segment not in [np.nan, -1]:
            segdf = get_ortools_solution_dataframe(segdf)
        
        # vehicle tag
        if 'vehicle' not in segdf.columns:
            segdf['vehicle'] = -1
        
        segdf.vehicle = (
            segdf.vehicle.fillna(-1).astype(int).astype(str) 
            + '_' + segdf[segmentation_col].fillna(-1).astype(int).astype(str)
        )
        
        not_segmented = (segdf[segmentation_col].isin([np.nan, 'nan', -1, None]))
        not_routed = (segdf.vehicle.str.split('_').str[0] == '-1')
        segdf.loc[not_segmented | not_routed, 'vehicle'] = None    
        
        result = result.append(segdf, sort=False)
        
    return result