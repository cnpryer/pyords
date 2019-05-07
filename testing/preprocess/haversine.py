from fyords.preprocess.distance import haversine, haversine_vectorized
import pandas as pd
import numpy as np


def test_haversine(data):
    lat1 = data.origin_lat.values[0]
    lon1 = data.origin_lon.values[0]
    lat2 = data.dest_lat.values[0]
    lon2 = data.dest_lon.values[0]
    return haversine_vectorized(
        lat1=lat1,
        lon1=lon1,
        lat2=lat2,
        lon2=lon2,
        unit='mi'
    )

def test_haversine_vectorized(data):
    lat1 = data.origin_lat.values
    lon1 = data.origin_lon.values
    lat2 = data.dest_lat.values
    lon2 = data.dest_lon.values
    return haversine_vectorized(
        lat1=lat1,
        lon1=lon1,
        lat2=lat2,
        lon2=lon2,
        unit='mi'
    )


if __name__ == '__main__':

    # generate testing lat and lon data
    data = pd.DataFrame({
        'origin_lat': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'origin_lon': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'dest_lat': np.random.uniform(low=-100.0, high=100.0, size=(10,)),
        'dest_lon': np.random.uniform(low=-100.0, high=100.0, size=(10,))
    })


    # haversine
    x = data.iloc[0]
    y = test_haversine(data)

    print(('\nTESTING (haversine)'
        '\ninput: {}'
        '\noutput: {}').format(x,y))

    # haversine_vectorized
    x = len(data)
    y = len(test_haversine_vectorized(data))

    print(('\nTESTING (haversine_vectorized)'
        '\ninput len: {}'
        '\noutput len: {}').format(x,y))
