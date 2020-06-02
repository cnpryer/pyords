from ..pyords.distance.matrix import haversine_distance_matrix
import pandas as pd
import numpy as np

def get_basic_routing_data():
    # generate testing lat and lon data
    return pd.DataFrame({
        'origin_lat': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'origin_lon': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'dest_lat': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'dest_lon': np.random.uniform(low=-100.0, high=100.0, size=(10,))})

def test_haversine_distance_matrix():
    data = get_basic_routing_data()
    lats = data.origin_lat.tolist() + data.dest_lat.tolist()
    lons = data.origin_lon.tolist() + data.dest_lon.tolist()
    distances = haversine_distance_matrix(lats=lats, lons=lons, unit='mi')
    assert isinstance(distances, (list,))
