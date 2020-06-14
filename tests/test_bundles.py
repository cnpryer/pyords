from pyords.cluster.implementations import (
    create_dbscan_expanded_clusters
)
from pyords.distance.haversine import create_haversine_matrix
import pyords as pyr

import pandas as pd
import numpy as np

from .common import TestConfig

class VrpVehicleCase:
    inputs = {
        'matrix': [[0, 1, 2], [1, 0, 2], [2, 2, 0]],
        'demand': [0, 3, 4],
        'max_vehicle_capacity': 5,
        'partitions': [1, 1, 1],
        'max_search_seconds': 30
    }

    outputs = {
        'vehicle_id': [1, 2]
    }

    implementation = None # TODO: pyr.ortools.vrp

    def run(self):
        bndl = pyr.VrpBundle(case=self)
        
        assert bndl.test()

        return self

def test_vrp_bundle_cases():
    vehicle_case = VrpVehicleCase().run()

# Create a Case
def test_vrp_bundle_partitioned():
    df = pd.read_csv(TestConfig.vrp_data_filepath)

    def init(dataframe:pd.DataFrame):
        lats, lons = dataframe.latitude, dataframe.longitude
        origins = [(41.4191, -87.7748)]
        matrix = create_haversine_matrix(origins, lats, lons)
        # unit is load for each node with demand (in this case
        # only destinations). inserting 0 at the front of the array
        demand = np.insert(dataframe.pallets.values, 0, 0)
    
        return matrix, demand

    # simplify euclidean distance calculation by projecting to positive vals
    x = df.latitude.values + 90
    y = df.longitude.values + 180
    df['cluster'] = create_dbscan_expanded_clusters(x, y)

    results = pd.DataFrame(columns=df.columns.tolist())
    for cluster in df.cluster.unique():
        clustered_df = df[df.cluster == cluster].copy().reset_index(drop=True)
        
        matrix, demand = init(clustered_df)
        bndl = pyr.VrpBundle(matrix=matrix, demand=demand)
        clustered_df = bndl.run().cast_solution_to_df(clustered_df)
        clustered_df.vehicle = str(int(cluster)) + '-' + clustered_df.vehicle.astype(int)\
            .astype(str)
        results = results.append(clustered_df, sort=False)

    assert len(results) == len(df)