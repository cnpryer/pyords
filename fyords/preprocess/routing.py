from .distance import haversine_vectorized

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
