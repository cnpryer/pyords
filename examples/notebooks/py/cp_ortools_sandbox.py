#!/usr/bin/env python
# coding: utf-8

# # Or-tools Implementation Development Sandbox
# The goal of this notebook is to establish an effective workflow for model engineering. 
# 
#   - Data Read
#   - Preprocessing
#     - geocoding
#     - distance processing
#     - clustering
#     - additional configuration
#   - Modeling
#   - Post-processing
#     - Scoring
#     
# Each of these components will be fleshed out from this notebook and refactored into a newer version of the pyords library. The current workflow is as follow:
# 
# 1. init notebook
# 2. script task
# 3. test task
# 4. complete objective
# 5. refactor into library using the same (if not more) tests

# In[ ]:


get_ipython().system('pip install ortools --upgrade')


# In[ ]:


import plotly.express as pe
import pandas as pd
import numpy as np
import os

this_dir = os.path.abspath('')
root_dir = os.path.dirname(this_dir)
print(root_dir)


# ## reading input shipment data
# Geocoding has been completed already. For initial versions scope is limited to contiguous US 5-digit zip codes. 

# In[ ]:


df = pd.read_csv('../../tests/vrp_testing_data.csv')

required_cols = ['weight', 'pallets', 'zipcode']
for col in required_cols: assert col in df.columns

df.head()


# In[ ]:


def get_plot(dataframe:pd.DataFrame, colors:str=None):
    return pe.scatter_geo(
        dataframe, 
        lat='latitude', 
        lon='longitude', 
        size='pallets',
        color=colors,
        scope='usa'
    )

get_plot(df)


# ## Preprocessing
# ### Distance processing
# For the ortools model setup the program needs to be fed a distance matrix that includes an origin node.

# In[ ]:


from haversine import haversine, Unit

def get_distance_matrix_from_dataframe(origins:list, dataframe:pd.DataFrame):
    # select an origin node

    distances = []
    for coords0 in origins + list(zip(dataframe.latitude, dataframe.longitude)):
        row = []
        for coords1 in origins + list(zip(df.latitude, df.longitude)):
            distance = haversine(coords0, coords1, unit=Unit.MILES)
            row.append(distance)
        distances.append(row)
        
    return distances


# ### Additional Processing
# As part of the modeling process we'll improve how we are preparing the data. To nail down effective logic to implement, I'll look to add processing here for **clustering** and **cluster improvements**.
# By clustering we can segment the problem up into realistic problem spaces. So far DBSCAN with ad-hoc mile-constrained chaining is used to pluck out nodes close enough together to even consider for one route (TODO: needs improvement).
# Once we have these clusters we can allow for additional flexibility in the overall solution by tweaking the segmentation determined by DBSCAN. Setting a fixed constraint of X miles might work initially, but there could be return routes, connecting stops, etc. that make one-offs more appealing.

# In[ ]:





# ## Or-tools modeling
# At this point the goal is to utilize ortools' cvrp wrappers. We are going to design this as a capacitated vrp without time windows or any complex penalties for the initial implementations.

# In[ ]:


from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

# inputs
# - distance matrix: graph defined as matrix 
#  (point to point; len(matrix) == number of unique nodes)
# - vehicle list: [max_cap, max_cap, max_cap] defined in units of demand
# - demand list: [units, units, units, ... n_distances]
# - max_solve_seconds
# - depot_index: poisition of node in definitions to use as origin node

# process vehicles input using total destination nodes count
# i.e. one truck available per stop


# constructing the model
def get_manager(distances:list, vehicles:list, depot_index:int): 
    return pywrapcp.RoutingIndexManager(len(distances), len(vehicles), 0)

def get_model(manager):
    return pywrapcp.RoutingModel(manager)

# config for optimization search
def get_search_params(max_solve_seconds:int=30):
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy =         routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.time_limit.seconds = max_solve_seconds
    
    return search_parameters

class MyPipe:
    def __init__(self, manager, model):
        self.manager = manager
        self.model = model
        self.model.SetArcCostEvaluatorOfAllVehicles(
            model.RegisterTransitCallback(self.distance_callback)
        )
        self.vehicles = None
        self.demand = None
        
    def distance_callback(self, i:int, j:int):
        """index of from (i) and to (j)"""
        node_i = self.manager.IndexToNode(i)
        node_j = self.manager.IndexToNode(j)

        return distances[node_i][node_j]
    
    def demand_callback(self, i:int):
        """capacity constraint"""
        node = self.manager.IndexToNode(i)

        return self.demand[node]
    
    def set_demand_callback(self):
        # add demand constraint using vehicles
        self.model.AddDimensionWithVehicleCapacity(
            # function which return the load at each location (cf. cvrp.py example)
            self.model.RegisterUnaryTransitCallback(self.demand_callback),
            0, # null capacity slack
            np.array([cap for cap in self.vehicles]), # vehicle maximum capacity
            True, # start cumul to zero
            'Capacity'
        )
        
        return self
    
    def add_vehicles(self, vehicles:list):
        self.vehicles = vehicles
        if self.demand: 
            return self.set_demand_callback()
        
        return self
    
    def add_demand(self, demand:list):
        self.demand = demand
        if self.vehicles: 
            return self.set_demand_callback()
        
        return self
    
    def get_solution(self, assignment):
        total_distance = 0
        total_load = 0
        solution = []
        for vehicle in range(len(self.vehicles)):
            i = self.model.Start(vehicle)
            info = {'vehicle': vehicle, 'stops': list(), 'stop_distances': [0],
                    'stop_loads': list()}

            while not self.model.IsEnd(i):
                node = self.manager.IndexToNode(i)
                info['stops'].append(node)
                info['stop_loads'].append(self.demand[node])

                previous_i = int(i)
                i = assignment.Value(self.model.NextVar(i))
                info['stop_distances'].append(self.model.GetArcCostForVehicle(previous_i, i, vehicle))

            # add return to depot to align with solution data
            info['stops'].append(0)
            info['stop_loads'].append(0)
            solution.append(info)
        
        return solution
            
    def run(self, search_params):
        return self.model.SolveWithParameters(search_params)
    
def get_solution_from_dataframe(dataframe:pd.DataFrame):
    # TODO: abstraction & testing
    origins = [(41.4191, -87.7748)] # assumed depot location for one-depot solutions
    distances = get_distance_matrix_from_dataframe(origins, dataframe)
    assert len(distances) == len(origins) + len(dataframe)
    
    vehicles = [26 for i in range(len(distances[1:]))]
    demand = np.insert(dataframe.pallets.values, 0, 0) # using pallets & adding 0 for the depot
    max_solve_seconds = 30
    depot_index = 0
    
    manager = get_manager(distances, vehicles, depot_index)
    model = get_model(manager)
    pipe = MyPipe(manager, model)
    search_params = get_search_params()
    assignment = pipe.add_vehicles(vehicles).add_demand(demand).run(search_params) 
    
    return pipe.get_solution(assignment)
        
solution = get_solution_from_dataframe(df)

assert len(solution) > 0 # TODO: create better solution testing

vehicleindex_w_moststops = np.argmax([len(v['stops']) for v in solution])
vehicles_w_loads = [v for v in solution if sum(v['stop_loads']) > 0]
print('total vehicles: %s' % len(solution))
print('total vehicles w loads: %s' % len(vehicles_w_loads))
#print('total load: %s' % solution[-1])
#print('total input load: %s' % demand.sum())
print('max stop sequence: %s' % solution[vehicleindex_w_moststops]['stops'])


# ## Post-processing
# **Scoring** a solution against a standardized formula/method will allow for more comprehensive testing, debugging, and model tuning. Scoring should be broken down into a **theory score** and a **practical score**. Theory scores will utilize theoretical expectations of vrp solutions (some assumptions about implementations needs to be made). The practical score will measure how implementable a solution is with respect to certain real-world expectations.  
# 
# For the sake of simplicity I'll use pandas as my target format and align scoring to get functions that pull from standard solution structs.

# In[ ]:


def process_solution_to_dataframe(solution:list, dataframe:pd.DataFrame):
    for v in solution:
        # accounting for insert of origin to matrix input
        stops = list(np.array(v['stops'][1:-1]) - 1)

        dataframe.loc[stops, 'vehicle'] = str(v['vehicle'])
        dataframe.loc[stops, 'sequence'] = list(range(len(stops))) # assumes order matches
        dataframe.loc[stops, 'stop_distance'] = v['stop_distances'][1:-1]
        dataframe.loc[stops, 'stop_loads'] = v['stop_loads'][1:-1]
    
    return dataframe
    
# scoring theoretical
# average capacity utilization of vehicles
def get_load_factor(solution:list):
    total_loads = sum([sum(s['stop_loads']) for s in solution])
    total_utilized_vehicles = len([s for s in solution if len(s['stops'][1:-1]) > 0])
    
    return total_loads/total_utilized_vehicles

def score_load_factor(dataframe:pd.DataFrame):
    return dataframe.groupby('vehicle').pallets.sum().mean()

# average distance traveled per vehicle
# NOTE: excluding distances returning to depot for now
# need to refactor for this.
def get_distance_factor(solution:list):
    total_distances = sum([sum(s['stop_distances'][:-1]) for s in solution])
    total_utilized_vehicles = len([s for s in solution if len(s['stops'][1:-1]) > 0])
    
    return total_distances/total_utilized_vehicles

def score_distance_factor(dataframe:pd.DataFrame):
    return dataframe.groupby('vehicle').stop_distance.sum().mean()

# average distance per stop
def score_travel_factor(dataframe:pd.DataFrame):
    return None

# ratio of one-stop routes to multi-stop 
# (assumption is that implementation is looking for multi-stops)
def score_multistop_factor(dataframe:pd.DataFrame):
    return None

# general service measured in total capacity serviced over total in scope
def score_multistop_factor(dataframe:pd.DataFrame):
    return None

# scoring practice
# deviation/distribution of stop distances per route
def score_erratic_distance_factor(dataframe:pd.DataFrame):
    return None

# measuring total number of moves across state boarders
def score_state_crossing_factor(dataframe:pd.DataFrame):
    return None

def postprocess_dataframe(dataframe:pd.DataFrame):
    # TODO: abstraction & testing

    load_factor = score_load_factor(dataframe)
    assert load_factor == get_load_factor(solution)

    distance_factor = score_distance_factor(dataframe)
    assert distance_factor == get_distance_factor(solution)

    stop_travel_factor = score_travel_factor(dataframe)
    multistop_factor = score_multistop_factor(dataframe)
    satisfaction_factor = score_multistop_factor(dataframe)
    erratic_distance_factor = score_erratic_distance_factor(dataframe)
    crossstate_factor = score_state_crossing_factor(dataframe)

    print('load_factor:', load_factor)
    print('distance_factor:', distance_factor)
    print('stop_travel_factor:', stop_travel_factor)
    print('multistop_factor:', multistop_factor)
    print('satisfaction_factor:', satisfaction_factor)
    print('erratic_distance_factor:', erratic_distance_factor)
    print('crossstate_factor:', crossstate_factor)
    
    return get_plot(dataframe, 'vehicle')

df = process_solution_to_dataframe(solution, df)
postprocess_dataframe(df)

