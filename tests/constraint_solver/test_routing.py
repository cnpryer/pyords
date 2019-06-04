from fyords.constraint_solver.routing import DedicatedFleet
from fyords.helpers.preprocess.routing import haversine_distance_matrix
import pandas as pd
import numpy as np


def test_basic_usage():
    # TODO: windows and other constraints
    # generate testing lat and lon data
    n = 10
    data = pd.DataFrame({
        'origin_lat': np.random.uniform(low=-100.0, high=100.0, size=(n,)),
        'origin_lon': np.random.uniform(low=-100.0, high=100.0, size=(n,)),
        'dest_lat': np.random.uniform(low=-100.0, high=100.0, size=(n,)),
        'dest_lon': np.random.uniform(low=-100.0, high=100.0, size=(n,)),
        'demand': np.random.randint(low=1, high=10, size=(n,))})

    # build locations list starting with origin (TODO: preprocessing multi-
    # origin routing models)
    locations = list([data[['origin_lat', 'origin_lon']].iloc[0].tolist()])

    # aggregate demand
    data = data.groupby(['origin_lat', 'origin_lon', 'dest_lat', 'dest_lon'])\
        .sum().reset_index()

    # append destinations with demand to locations
    locations += list(zip(data.dest_lat.tolist(), data.dest_lon.tolist()))
    locations = np.array([np.array(loc) for loc in locations]) # convert tuples

    # build demands
    demands = np.array([0] + data.demand.tolist())

    # build distance matrix
    lats = np.array([loc[0] for loc in locations])
    lons = np.array([loc[1] for loc in locations])
    distances = np.array(haversine_distance_matrix(lats, lons, 'mi'))

    # TODO: build time windows
    windows = np.array([np.nan for loc in locations])

    # build vehicles
    vehicles = np.array([45 for i in range(0, 2)])

    routes = DedicatedFleet(
        distances=distances,
        windows=windows,
        demands=demands,
        vehicles=vehicles)

    assert routes is not None