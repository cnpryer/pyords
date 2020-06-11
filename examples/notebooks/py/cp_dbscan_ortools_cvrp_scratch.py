#!/usr/bin/env python
# coding: utf-8

# In[ ]:


get_ipython().run_line_magic('load_ext', 'autoreload')
get_ipython().run_line_magic('autoreload', '2')


# In[ ]:


get_ipython().system('pip install pyords --upgrade')
get_ipython().system('pip install plotly')
get_ipython().system('pip install ortools --upgrade')


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


clusters_ranking = df.groupby('cluster')['pallets'].median().sort_values()
clusters_ranking


# In[ ]:


from pyords.distance.matrix import ovrp_haversine_distance_matrix
from pyords.solver.helpers import OrtoolsCvrpDataFrame, ovrp_to_df
from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# inputs
distances = ovrp_haversine_distance_matrix(
    lats=df.latitude.values, lons=df.longitude.values, unit='mi')
vehicles = [26]*len(distances)
demand = np.insert(df.pallets.values, 0, 0)

# scripting ortools model construction & method.
manager = pywrapcp.RoutingIndexManager(len(distances), len(vehicles), 0)

def distance_callback(i:int, j:int):
    """index of from (i) and to (j)"""
    node_i = manager.IndexToNode(i)
    node_j = manager.Inde-xToNode(j)
    
    return distances[node_i][node_j]

# model construction
model = pywrapcp.RoutingModel(manager)
model.SetArcCostEvaluatorOfAllVehicles(
    model.RegisterTransitCallback(distance_callback)
)

def demand_callback(i:int):
    """capacity constraint"""
    node = manager.IndexToNode(i)
    
    return demand[node]

model.AddDimensionWithVehicleCapacity(
    # function which return the load at each location (cf. cvrp.py example)
    model.RegisterUnaryTransitCallback(demand_callback),
    
    0, # null capacity slack
    np.array([cap for cap in vehicles]), # vehicle maximum capacity
    True, # start cumul to zero
    'Capacity'
)

# config for optimization search
search_parameters = pywrapcp.DefaultRoutingSearchParameters()
search_parameters.first_solution_strategy =     routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
search_parameters.time_limit.seconds = 30

assignment = model.SolveWithParameters(search_parameters)

def get_solution():
    total_distance = 0
    total_load = 0
    solution = []
    for vehicle in range(len(vehicles)):
        i = model.Start(vehicle)
        info = {'vehicle': vehicle, 'route': '', 'stops': set()}
        route_distance = 0
        route_load = 0
        while not model.IsEnd(i):
            node = manager.IndexToNode(i)
            route_load += demand[node]
            info['route'] += ' {0} Load({1})'.format(node, route_load)
            previous_i = i
            i = assignment.Value(model.NextVar(i))
            route_distance += model.GetArcCostForVehicle(
                previous_i, i, vehicle)
            info['stops'].add(node)
        info['route'] += ' {0} Load({1})'.format(
            manager.IndexToNode(i), route_load)
        info['route'] = info['route'][1:] # strip leading zero
        info['dist'] = route_distance
        info['load'] = route_load
        solution.append(info)
        total_distance += route_distance
        total_load += route_load
    solution.append({'total dist': total_distance})
    solution.append({'total load': total_load})
        
    return solution

solution = get_solution()

output_vehicles = solution[:-2] # TODO: fix this
vehicleindex_w_moststops = np.argmax([len(v['stops']) for v in output_vehicles])
vehicles_w_loads = [v for v in output_vehicles if v['load'] > 0]
print('total vehicles: %s' % len(output_vehicles))
print('total vehicles w loads: %s' % len(vehicles_w_loads))
print('total load: %s' % solution[-1])
print('total input load: %s' % demand.sum())
print('max stop sequence: %s' % output_vehicles[vehicleindex_w_moststops]['stops'])


# In[ ]:


for vehicle in vehicles_w_loads:
    locs = np.array(list(vehicle['stops'])[1:]) - 1
    df.loc[locs, 'vehicle'] = vehicle['vehicle']

# look at multistop vehicles
multistop_vehicles =     [int(v['vehicle']) for v in vehicles_w_loads if len(v['stops']) > 2]

def plot(dataframe:pd.DataFrame, trace_by:pd.Series):
    return pe.scatter_geo(
        dataframe, 
        lat='latitude', 
        lon='longitude', 
        size='pallets', 
        scope='usa',
        color=trace_by
    )
    
plot(
    df.loc[df.vehicle.fillna(-1).astype(int).isin(multistop_vehicles)],
    df.loc[df.vehicle.fillna(-1).astype(int).isin(multistop_vehicles)].vehicle.astype(str)
)

