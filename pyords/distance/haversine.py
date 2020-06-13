from math import radians, cos, sin, asin, sqrt
import numpy as np
import random

from haversine import haversine, Unit

def pyords_haversine(lat1: float, lon1: float, lat2: float, lon2: float,
              unit: str='mi'):
    """Calculate the great circle distance between two points on the earth.

    Parameters
    ----------
    lat1: float of origin latitude.
    lon1: float of origin longitude.
    lat2: float of destination latitude.
    lon2: float of destination longitude.
    unit: string of distance unit of measure ('mi', 'km').

    Returns
    -------
    distance: float
    """
    # convert decimal degrees to radians
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    c = 2 * asin(sqrt(a))

    r = {
        'mi': 3956,
        'km': 6371
    }[unit]

    return c * r

def pyords_haversine_vectorized(lat1: list, lat2: list, lon1: list, lon2: list,
                         unit: str='mi'):
    """Calculate the great circle distance between coordinates of two vectors
    on the earth; order of origin->destination. This function expects
    np.ndarrays instead of python lists. TODO: need to refactor for this.

    Parameters
    ----------
    lat1: list-like of origin latitude.
    lon1: list-like of origin longitude.
    lat2: list-like of destination latitude.
    lon2: list-like of destination longitude.
    unit: string of distance unit of measure ('mi', 'km').

    Returns
    -------
    distances: np.ndarray
    """
    # TODO: degrees?
    lat1 = np.radians(lat1)
    lon1 = np.radians(lon1)
    lat2 = np.radians(lat2)
    lon2 = np.radians(lon2)

    # haversine formula
    dlon = lon2 - lon1
    dlat = lat2 - lat1

    # TODO: port to numpy
    a = np.sin(dlat/2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2)**2
    c = 2 * np.arcsin(np.sqrt(a))

    r = {
        'mi': 3956,
        'km': 6371
    }[unit]

    return c * r

def create_haversine_matrix(origins:list, latitudes:list, longitudes:list):
    distances = []
    destinations = list(zip(latitudes, longitudes))
    for coords0 in origins + destinations:
        row = []
        for coords1 in origins + destinations:
            distance = haversine(coords0, coords1, unit=Unit.MILES)
            row.append(distance)
        distances.append(row)
        
    return distances


def pyords_haversine_distance_matrix(lats, lons, unit: str='mi'):
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
        distances = pyords_haversine_vectorized(
                lat1=origin_lats,
                lon1=origin_lons,
                lat2=lats,
                lon2=lons,
                unit=unit)
        distance_matrix.append(list(distances))
    return distance_matrix

def ortools_haversine_distance_matrix(lats, lons, unit: str='mi'):
    """Generate a distance matrix for the ovrp (open vehicle routing/no return
    depot). The matrix begins with a dummy node that has 0 distance to and from
    all other nodes."""
    lats_arr = np.array(lats)
    lons_arr = np.array(lons)
    lats_li = list(np.insert(lats, 0, np.nan))
    lons_li = list(np.insert(lons, 0, np.nan))
    matrix_arr = np.nan_to_num(pyords_haversine_distance_matrix(lats, lons, unit))
    matrix_li = [list(arr) for arr in matrix_arr]
    
    return matrix_li