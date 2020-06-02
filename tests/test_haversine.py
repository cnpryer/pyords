from ..pyords.distance.haversine import haversine, haversine_vectorized
import pandas as pd
import numpy as np


def get_basic_routing_data():
    # generate testing lat and lon data
    return pd.DataFrame({
        'origin_lat': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'origin_lon': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'dest_lat': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'dest_lon': np.random.uniform(low=-100.0, high=100.0, size=(10,))})

def test_data_initialization():
    assert isinstance(get_basic_routing_data(), (pd.DataFrame,))

def test_haversine():
    data = get_basic_routing_data()
    lat1 = data.origin_lat.values[0]
    lon1 = data.origin_lon.values[0]
    lat2 = data.dest_lat.values[0]
    lon2 = data.dest_lon.values[0]
    distances = haversine(
        lat1=lat1,
        lon1=lon1,
        lat2=lat2,
        lon2=lon2,
        unit='mi')
    assert isinstance(distances, (float,))

def test_haversine_vectorized():
    data = get_basic_routing_data()
    lat1 = data.origin_lat.values
    lon1 = data.origin_lon.values
    lat2 = data.dest_lat.values
    lon2 = data.dest_lon.values
    distances =  haversine_vectorized(
        lat1=lat1,
        lon1=lon1,
        lat2=lat2,
        lon2=lon2,
        unit='mi')
    assert isinstance(distances, (np.ndarray,))
