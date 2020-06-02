from math import radians, cos, sin, asin, sqrt
import numpy as np

def haversine(lat1: float, lon1: float, lat2: float, lon2: float,
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

def haversine_vectorized(lat1: list, lat2: list, lon1: list, lon2: list,
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
