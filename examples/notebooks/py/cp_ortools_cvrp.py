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

# scripting out ortools model construction and run
# df: dataframe input containing every shipment.
# distances: distance matrix of all point to point calculations.
#  [[n0-n0, n0-n1, n0-n2, n0-n3], [...], ...]
# vehicles: matrix for truck definition.
#  [[t0_min_weight, t0_max_weight], [...], ...]
# demand: array of demand (includes origin? TODO: validate).

df = pd.read_csv('../../tests/vrp_testing_data.csv')[:20]
distances = ovrp_haversine_distance_matrix(
    lats=df.latitude.values, lons=df.longitude.values, unit='mi')
vehicles = [[0, 26]]*1
demand = np.insert(df.pallets.values, 0, 0)

# NOTE: for refactor need to make construction of the above elements
# more explicit.
def test_pyords():
    cvrp = GoogleORCVRP(distances=distances, demand=demand,
        vehicles=vehicles, depot=0, max_seconds=30)
    cvrp.solve()

    assert len(cvrp.solution) > 0


# In[ ]:


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# scripting ortools model construction & method.
manager = pywrapcp.RoutingIndexManager(len(distances), len(vehicles), 0)

def distance_callback(i:int, j:int):
    """index of from (i) and to (j)"""
    node_i = manager.IndexToNode(i)
    node_j = manager.IndexToNode(j)
    
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
    np.array([caps[1] for caps in vehicles]), # vehicle maximum capacity
    True, # start cumul to zero
    'Capacity'
)

for i, vehicle in enumerate(vehicles):
    model.GetDimensionOrDie('Capacity')        .CumulVar(model.End(i)).RemoveInterval(0, int(vehicle[0]))

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

get_solution()


# In[ ]:


from haversine import haversine, Unit

distances = []
for coords0 in list(zip(df.latitude, df.longitude)):
    for coords1 in list(zip(df.latitude, df.longitude)):
        distance = haversine(coords0, coords1, unit=Unit.MILES)
        print(distance)

