#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


from pyords.cluster.algorithms import DBSCAN
import plotly.express as pe
import pandas as pd
import numpy as np
import os
# TODO: https://developers.google.com/optimization/routing/routing_tasks#setting-start-and-end-locations-for-routes
# TODO: all shipments must end at 41.390800, -88.144599


# In[ ]:


this_dir = os.path.abspath('')
this_dir


# In[ ]:


root_dir = os.path.dirname(this_dir)
root_dir


# In[ ]:


filepath = os.path.join('../../tests/vrp_testing_data.csv')
df = pd.read_csv(filepath)
df.head()


# In[ ]:


pe.scatter_geo(df, lat='latitude', lon='longitude', size='pallets', scope='usa')


# In[ ]:


epsilon = 0.79585 # approximate degree delta for 50 miles
minpts = 2 # at least cluster 2

# simplify euclidean distance calculation by projecting to positive vals
x = df.latitude.values + 90
y = df.longitude.values + 180

dbscan = DBSCAN(epsilon, minpts)
dbscan.fit(x, y)
dbscan.predict()
df['cluster'] = dbscan.clusters
pe.scatter_geo(df, lat='latitude', lon='longitude', size='pallets', scope='usa',
              color='cluster')


# In[ ]:


from pyords.distance.matrix import ovrp_haversine_distance_matrix
from pyords.solver.helpers import GoogleORCVRP, ovrp_to_df


# In[ ]:


clusters_ranking = df.groupby('cluster')['pallets'].median().sort_values()
clusters_ranking


# In[ ]:


import pprint

def solve(dataframe:pd.DataFrame):
    """
    # scripting out ortools model construction and run
    # df: dataframe input containing every shipment.
    # distances: distance matrix of all point to point calculations.
    #  [[n0-n0, n0-n1, n0-n2, n0-n3], [...], ...]
    # vehicles: matrix for truck definition.
    #  [[t0_min_weight, t0_max_weight], [...], ...]
    # demand: array of demand (includes origin? TODO: validate).
    """
    distances = ovrp_haversine_distance_matrix(
        lats=dataframe.latitude.values,
        lons=dataframe.longitude.values,
        unit='mi'
    )
    demand = np.insert(dataframe.pallets.values, 0, 0)
    avg_demand = np.mean(demand[1:])
    vehicles = [[0, 26]]*10
    cvrp = GoogleORCVRP(
        distances=distances,
        demand=demand,
        vehicles=vehicles, 
        depot=0, 
        max_seconds=30
    )
    cvrp.solve()
    
    return cvrp.solution


# In[ ]:


solution_count = 1
shipment_ids = np.zeros(len(df), dtype=np.int32) - 1
for cluster in df.cluster.unique():
    if cluster >= 0:
        _df = df.loc[df.cluster == cluster]
        print(_df.head(), '\n')
        
        solution = solve(_df)
        
        tmp_shipment_ids = ovrp_to_df(_df, solution) * solution_count
        indicies = _df.index.tolist()
        for i, _id in enumerate(tmp_shipment_ids):
            index = indicies[i]
            if _id > 0:
                shipment_ids[index] = _id
            
        solution_count += 1


# In[ ]:


cluster = 3
solution = solve(df[df.cluster == cluster])
solution_str = pprint.pformat(solution)
print(cluster, solution_str, '\n')

