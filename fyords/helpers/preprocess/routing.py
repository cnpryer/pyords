from .distance import haversine_vectorized
import numpy as np
import pandas as pd
import random

def haversine_distance_matrix(lats: list, lons: list, unit: str='mi'):
    """Generate a matrix of all-to-all disances using a vectorized haversine
    calculation. Order is preserved. This means that the index of lats
    corresponds to each location's index in the matrix.

    Parameters
    ----------
    lats: list-like of location latitudes.
    lons: list-like of location longitudes.
    unit: string of distance unit of measure ('mi', 'km').

    Returns
    -------
    matrix or list of lists: 2d list
    """
    locations = list(zip(lats, lons))
    n = len(locations)
    distance_matrix = []
    for i, location in enumerate(locations):
        origin_lats = [location[0]]*n
        origin_lons = [location[1]]*n
        distances = haversine_vectorized(
                lat1=origin_lats,
                lon1=origin_lons,
                lat2=lats,
                lon2=lons,
                unit=unit)
        distance_matrix.append(list(distances))
    return distance_matrix

def encode_random_dedicatedfleet_ga(distances: list, size: int):
    """Generate randomized encoded population of route sets (individuals) to
    optimize using a genetic algorithm.

    Parameters
    ----------
    distances: distance matrix where each index represents a node within scope.
    size: population size desired.

    Returns
    -------
    list of lists of lists where each index is an individual consisting of a
    potential solution to the routing problem. In other words, each individual
    of the population is initialized to a random set of routes (elements are
    location indices and order demonstrates stop order), each of a random
    length: list
    """
    population = []
    N = len(distances)-1
    for i in range(0, size): # per individual
        individual = []
        for j in range(0, random.randint(1, N)): # random len of individual
            routes = \
                np.random.randint(low=1, high=N, size=(random.randint(1, N),))
            individual.append(list(routes))
        population.append(individual)
    return population
