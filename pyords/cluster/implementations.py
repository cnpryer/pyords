from .algorithms import DBSCAN
import pandas as pd


def get_dbscan_clusters(dataframe:pd.DataFrame):
    """
      weight,pallets,zipcode,latitude,longitude
      18893,24,46168,39.6893,-86.3919
      19599,25,46168,39.6893,-86.3919
    
    return df with clusters col
    """
    epsilon = 0.79585 # approximate degree delta for 50 miles
    minpts = 2 # at least cluster 2

    # simplify euclidean distance calculation by projecting to positive vals
    x = dataframe.latitude.values + 90
    y = dataframe.longitude.values + 180

    dbscan = DBSCAN(epsilon, minpts)
    dbscan.fit(x, y)
    dbscan.predict()
    dataframe['cluster'] = dbscan.clusters

    return dataframe