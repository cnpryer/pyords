from .distance import haversine_vectorized
import numpy as np
import pandas as pd
import random

def haversine_distance_matrix(lats:list, lons:list, unit:str='mi'):
    '''
    Purpose:
        Generate a matrix of all-to-all disances using a vectorized haversine
        calculation.

    Args:
        lats, lons: lists of location latitudes. Order is preserved.
        unit: options are 'mi', 'km'
    '''
    locations = list(zip(lats, lons))
    n = len(locations)
    distance_matrix = []
    for i, location in enumerate(locations):
        origin_lats = [location[0]]*n
        origin_lons = [location[1]]*n
        distance_matrix.append(
            haversine_vectorized(
                lat1=origin_lats,
                lon1=origin_lons,
                lat2=lats,
                lon2=lons,
                unit=unit
            )
        )
    return distance_matrix

def encode_random_dedicatedfleet_ga(distances:np.array, size:int):
    '''
    Purpose:
        Return randomized encoded population of route sets (individuals) to
        optimize using a genetic algorithm.

    Args:
        distances: distance matrix where each index represents a node within
        scope.
        size: population size desired.

    TODO:
        Abstract to encoding.py?
    '''
    population = []
    N = len(distances)-1
    for i in range(0, size): # per individual
        individual = []
        for j in range(0, random.randint(1, N)): # random len of individual
            individual.append(
                np.random.randint(low=1, high=N, size=(random.randint(1, N),))
            )
        population.append(np.array(individual))
    return np.array(population)

def encode_clustered_dedicatedfleet_ga(data:pd.DataFrame):
    '''
    Purpose:
        Return an encoded, clustered population to optimize using a genetic
        algorithm

    Args:
        data: dataframe of demand with various features for clustering.

    TODO:
        Abstract to encoding.py?
    '''
    pass
