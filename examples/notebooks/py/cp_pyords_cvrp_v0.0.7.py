#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


import pyords as ps
print(ps.__version__) # TODO: target for 0.0.7

import plotly.express as pe
import pandas as pd
import numpy as np
import os
# TODO: https://developers.google.com/optimization/routing/routing_tasks#setting-start-and-end-locations-for-routes
# TODO: all shipments must end at 41.390800, -88.144599


# # using pyords for shipment optimization
# 
# ```python
# import pyords as pyr
# 
# df = pd.read_csv('../../tests/vrp_testing_data.csv')
# vrp = pyr.OrToolsVrpBamboo(df, demand='pallets', inline=True)
# vrp.map
# 
# x = df.latitude
# y = df.longitude
# clustering = pyr.DBSCAN(x, y, project_data=True)
# df['clusters'] = clustering.clusters
# 
# pymap = vrp.swap(df)
# vrp.show(show_clusters=True)
# 
# clustering = clustering.expand('closest')
# df.clusters = clustering.clusters
# 
# vrp = vrp.swap(df)
# vrp.show(show_clusters=True)
# 
# origins = get_my_origins()
# destinations = vrp.distance_matrix
# df['solution_1'] = vrp.route(origins, vehicles)
# 
# df['solution_2'] = vrp.route(origins, vehicles, limit_by='clusters')
# 
# vrp.logs
# ```
