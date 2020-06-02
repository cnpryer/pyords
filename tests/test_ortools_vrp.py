from ..pyords.distance.matrix import ovrp_haversine_distance_matrix
from ..pyords.solver import GoogleORCVRP
import pandas as pd
import numpy as np
import logging
from os import path

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

def test_basic_cvrp():
    df = pd.read_csv(path.join(this_dir, 'vrp_testing_data.csv'))[:20]
    distances = ovrp_haversine_distance_matrix(
        lats=df.latitude.values, lons=df.longitude.values, unit='mi')
    vehicles = [[1, 100]]*10
    demand = np.insert(df.pallets.values, 0, 0)
    cvrp = GoogleORCVRP(distances=distances, demand=demand,
        vehicles=vehicles, depot=0, max_seconds=30)
    cvrp.solve()
    logging.info('cvrp configuration: %s' % cvrp.to_dict())
    logging.info('solution: %s' % cvrp.solution)
    assert len(cvrp.solution) > 0
