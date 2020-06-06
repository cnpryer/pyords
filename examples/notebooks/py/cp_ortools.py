#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().system('pip install ortools')


# In[ ]:


get_ipython().system('pip install pyords')


# In[ ]:


from pyords.distance.matrix import ovrp_haversine_distance_matrix
from pyords.solver.helpers import GoogleORCVRP

import pandas as pd
import numpy as np

df = pd.read_csv('../../tests/vrp_testing_data.csv')[:20]
distances = ovrp_haversine_distance_matrix(
    lats=df.latitude.values, lons=df.longitude.values, unit='mi')
vehicles = [[1, 100]]*10
demand = np.insert(df.pallets.values, 0, 0)
cvrp = GoogleORCVRP(distances=distances, demand=demand,
    vehicles=vehicles, depot=0, max_seconds=30)
cvrp.solve()
'cvrp configuration: %s' % cvrp.to_dict()
'solution: %s' % cvrp.solution

assert len(cvrp.solution) > 0

