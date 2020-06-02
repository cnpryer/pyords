from .haversine import haversine_vectorized
import numpy as np
import pandas as pd
import random

def haversine_distance_matrix(lats, lons, unit: str='mi'):
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

def ovrp_haversine_distance_matrix(lats, lons, unit: str='mi'):
    """Generate a distance matrix for the ovrp (open vehicle routing/no return
    depot). The matrix begins with a dummy node that has 0 distance to and from
    all other nodes."""
    lats_arr = np.array(lats)
    lons_arr = np.array(lons)
    lats_li = list(np.insert(lats, 0, np.nan))
    lons_li = list(np.insert(lons, 0, np.nan))
    matrix_arr = np.nan_to_num(haversine_distance_matrix(lats, lons, unit))
    matrix_li = [list(arr) for arr in matrix_arr]
    return matrix_li
