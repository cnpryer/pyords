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


# # using pyords bundles for vehicle optimization
# 
# ```python
# import pyords as pyr
# 
# 
# df = pd.read_csv('my_shipment_data.csv')
# bundle = pyr.OrVrpBundle(zips=df.zipcodes, demand=df.pallets)
# 
# solution = bundle.run( # get list of vehicles from vrp task
#     depot_index=0, # required
#     max_vehicle_capacity=26, # default: 26
#     max_search_seconds=30, # default 30
#     segment_by=my_clusters, # optional TODO: allow for distributed
#     return_solution=True # optional
# )
# 
# live_vehicles_returned = [s for s in solution if len(s['stops'][1:-1]) > 0]
# 
# assert bundle.vehicles.pull('n.utilized') == len(live_vehicles_returned)
# 
# df['vehicles'] = bundle.pull('vehicles')
# ```
# 
# # pyords bundles
# Bundles are self-contained problem definitions that can be tuned with the pyords tool libraries and other more popular python libraries. Bundles are input-output blueprinted objects for solving problems in a python environment. Bamboo bundles are used to branch pyords functionality from dataframes. Pyords bundle fundementals are similar in nature to tasks. A bundle can be initiated with input and completed with parameters.
