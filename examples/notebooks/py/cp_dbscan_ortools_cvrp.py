#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


from pyords.cluster.algorithms import DBSCAN
from pyords.distance.matrix import ovrp_haversine_distance_matrix
from pyords.solver.helpers import OrtoolsCvrpDataFrame, ovrp_to_df
from pyords import __version__
print(__version__)

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


epsilon = 1.79585 # approximate degree delta for 50 miles
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


clusters_ranking = df.groupby('cluster')['pallets'].median().sort_values()
clusters_ranking


# In[ ]:


def get_ortools_solution_dataframe(dataframe:pd.DataFrame):
    """
    # scripting out ortools model construction and run
    # df: dataframe input containing every shipment.
      weight,pallets,zipcode,latitude,longitude
      18893,24,46168,39.6893,-86.3919
      19599,25,46168,39.6893,-86.3919
    # distances: distance matrix of all point to point calculations.
    #  [[n0-n0, n0-n1, n0-n2, n0-n3], [...], ...]
    # vehicles: matrix for truck definition.
    #  [[t0_min_weight, t0_max_weight], [...], ...]
    # demand: array of demand (includes origin? TODO: validate).

    TODO: return dataframe with vehicle col
    """
    dataframe = dataframe.reset_index(drop=True)
    app = OrtoolsCvrpDataFrame(
        dataframe.copy(),
        depot_index=0, 
        max_solve_seconds=30
    )
    app.solve()    

    return app.df

def get_many_ortools_solutions_dataframe(dataframe:pd.DataFrame, segmentation_col:str):
    result = pd.DataFrame(columns=dataframe.columns.tolist()+['vehicle'])
    
    # TODO: create concurrent tasks for segment optimizations
    for segment in dataframe[segmentation_col].unique():
        segdf = dataframe[dataframe[segmentation_col] == segment].copy()
        
        if segment not in [np.nan, -1]:
            segdf = get_ortools_solution_dataframe(segdf)
        
        # vehicle tag
        if 'vehicle' not in segdf.columns:
            segdf['vehicle'] = -1
        
        segdf.vehicle = (
            segdf.vehicle.fillna(-1).astype(int).astype(str) 
            + '_' + segdf[segmentation_col].fillna(-1).astype(int).astype(str)
        )
        
        not_clustered = (segdf.cluster.isin([np.nan, 'nan', -1, None]))
        not_routed = (segdf.vehicle.str.split('_').str[0] == '-1')
        segdf.loc[not_clustered | not_routed, 'vehicle'] = None    
        
        result = result.append(segdf, sort=False)
        
    return result


# In[ ]:


#result = get_many_ortools_solutions_dataframe(df, 'cluster')
result = get_ortools_solution_dataframe(df)
max_stop_vehicle = result.groupby('vehicle').size().sort_values(ascending=False).index[0]
result[result.vehicle == max_stop_vehicle]


# In[ ]:


result.vehicle = result.vehicle.astype(str)
pe.scatter_geo(result, lat='latitude', lon='longitude', size='pallets', scope='usa',
              color='vehicle')


# In[ ]:


result2 = get_many_ortools_solutions_dataframe(df, 'cluster')

print('without dbscan:', result.groupby('vehicle').pallets.sum().mean())
print('with dbscan:', result2.groupby('vehicle').pallets.sum().mean())

