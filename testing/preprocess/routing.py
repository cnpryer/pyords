from fyords.util.preprocess.routing import (
    haversine_distance_matrix,
    encode_random_dedicatedfleet_ga
)
import pandas as pd
import numpy as np

def test_encode_random_dedicatedfleet_ga(data):
    return encode_random_dedicatedfleet_ga(data, 100)

def test_haversine_distance_matrix(lats, lons):
    return haversine_distance_matrix(
        lats=lats,
        lons=lons,
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

    # TODO: improve
    lats = (
        data.origin_lat.tolist()
        +data.dest_lat.tolist()
    )
    lons = (
        data.origin_lon.tolist()
        +data.dest_lon.tolist()
    )

    # haversine
    distances = test_haversine_distance_matrix(lats, lons)
    x = len(list(zip(lats, lons)))
    y = len(distances)

    print(('\nTESTING (haversine_distance_matrix)'
        '\ninput: {}'
        '\noutput: {}').format(x,y))

    # dedicatedfleet encoding (random)
    population = test_encode_random_dedicatedfleet_ga(distances)
    x = len(distances)
    y = len(population)

    print(('\nTESTING (encode_random_dedicatedfleet_ga)'
        '\ninput: {}'
        '\noutput: {}').format(x,y))
