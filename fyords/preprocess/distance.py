from math import radians, cos, sin, asin, sqrt
import numpy as np

def haversine(lat1:float, lat2:float, lon1:float, lon2:float, unit:str='mi'):
    '''
    Purpose:
        Calculate the great circle distance between two points
        on the earth.

    Args:
        ...
        unit: options are 'mi', 'km'
    '''
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

def haversine_vectorized(lat1:np.array, lat2:np.array, lon1:np.array,
lon2:np.array, unit:str='mi'):
    '''
    Purpose:
        Calculate the great circle distance between coordinates of two vectors
        on the earth; order of origin->destination.

    Args:
        c1, c2: [lat:float, lon:float]
        unit: options are 'mi', 'km'
    '''
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
