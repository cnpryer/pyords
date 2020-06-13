from .algorithms import DBSCAN
import pandas as pd
import numpy as np

def add_closest_clusters(x:list, y:list, clusters:list):
    """
    Takes a list of x, a list of y, and a list of clusters to
    process clusters for x, y without an assigned cluster.
    To accomplish this the function calculates the euclidean
    distance to every node with a cluster. It will then assign
    the found node's cluster as its own.
    
    x: list-like of x coordinates
    y: list-like of y coordinates
    clusters: list-like of clusters assigned
    
    return list of clusters
    """
    c = list(clusters)
    
    positions = list(range(len(c)))
    missing_clusters = [i for i in positions if pd.isnull(c[i])]
    has_clusters = [i for i in positions if i not in missing_clusters]
    
    x_copy = np.array(x, dtype=float)
    x_copy[missing_clusters] = np.inf

    y_copy = np.array(y, dtype=float)
    y_copy[missing_clusters] = np.inf
    
    for i in missing_clusters:
        x_deltas = abs(x[i] - x_copy)
        y_deltas = abs(y[i] - y_copy)
        deltas = x_deltas + y_deltas
        
        c[i] = c[np.argmin(deltas)]
    
    return c

def create_dbscan_basic(x:list, y:list):
    epsilon = 0.79585 # approximate degree delta for 50 miles
    minpts = 2 # at least cluster 2

    dbscan = DBSCAN(epsilon, minpts)
    dbscan.fit(x, y)
    dbscan.cluster()
    
    return dbscan

def create_dbscan_expanded_clusters(x:list, y:list):   
    dbscan = create_dbscan_basic(x, y)
    
    # add those without an assigned cluster
    # to their closest cluster
    clusters = [c if int(c) >= 0 else None for c in dbscan.clusters]
    clusters = add_closest_clusters(x, y, clusters)
    
    return clusters