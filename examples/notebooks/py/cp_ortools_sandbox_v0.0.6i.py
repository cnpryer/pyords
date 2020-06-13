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
# 
# ## Feature Implementations
# The goal is to design the implementations of each feature as simple as possible but allow for clear package utilization. As each feature is utilized they will be improved upon. Each implementation should have benefits documented for its support:
# 
# 
# ### Distance Processing
# For Ortools integration, distance matricies define most of the model setup. Initially every model will be limited to inputs of only destinations that'd be serviced by a given, single origin. To use the function, pass the origin(s) (NOTE: pyords ortools integration will be limited to one origin node designs) and destinations to that returns a position-defined network of nodes using straight-line distances from lats and lons. This function can serve as one input implementation for ortools integration.
# 
# I'm just going to add the function as is to the library within the distance namespace. No embedded implementation for this distance processing.
# 
# ### Cluster Processing
# DBSCAN is a recognized clustering method. A DBSCAN class can implement the more pure implementations of this clustering in pyords. The one added customization piece to this feature is the ability to expand clusters (and in turn problem space). This function can be implemented as a stand-alone branch of the library for the future of its cluster toolset.
# 
# I'll add this as a DBSCAN class under the cluster namespace to keep it simple. I will add an adjacent function for processing closest clusters (TODO: nearest neighbor optimization). An embedded implementation function using each of the cluster processing methods here will be added to the namespace as well.
# 
# ### Ortools Modeling
# Typically ortools is utilized in script-like programs. This means that your enviroment is restricted to the purpose of your notebook. In order to effectively partition the integration from the enviroment the integration may be used as par of, pyords can provide light wrappers for the existing ortools wrappers. These wrappers will aid in task-like processing for ortools models. Testing can be done by class and allow for embedded statistics early on in the development of this library (NOTE: pyords is developed alongside any project requiring certain dependencies; [see cvrp-app](https://github.com/christopherpryer/cvrp-app)).
# 
# **OrToolsPipe** will be added for classed instances of ortools managers, models, and related data to orchestrate the optimization wrappers.
# **OrToolsChecksStage** will be added for solution & dataframe cross-validation testing & reporting.
# 
# TODO: create OrToolsTask
# 
# There will be an embedded implementation function for this feature.
# 
# ### Post-processing
# TODO: shipment optimization post-processing can be added to the library after it's been abstracted from ortools.

# In[ ]:


import plotly.express as pe
import pandas as pd
import numpy as np
import os


# ## reading input shipment data
# Geocoding has been completed already. For initial versions scope is limited to contiguous US 5-digit zip codes. 

# In[ ]:


df = pd.read_csv('../../tests/vrp_testing_data.csv')

required_cols = ['weight', 'pallets', 'zipcode']
for col in required_cols: assert col in df.columns
    
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

def create_distances_matrix(origins:list, latitudes:list, longitudes:list):
    distances = []
    destinations = list(zip(latitudes, longitudes))
    for coords0 in origins + destinations:
        row = []
        for coords1 in origins + destinations:
            distance = haversine(coords0, coords1, unit=Unit.MILES)
            row.append(distance)
        distances.append(row)
        
    return distances

def test_create_distances_matrix():
    origins = [(0, 1)]
    latitudes = [1, 2, 3, 4]
    longitudes = [1, 2, 3, 4]
    matrix = create_distances_matrix(origins, latitudes, longitudes)
    
    assert len(matrix) == len(origins) + len(latitudes)
    
test_create_distances_matrix()


# ### Additional Processing
# As part of the modeling process we'll improve how we are preparing the data. To nail down effective logic to implement, I'll look to add processing here for **clustering** and **cluster improvements**.
# By clustering we can segment the problem up into realistic problem spaces. So far DBSCAN with ad-hoc mile-constrained chaining is used to pluck out nodes close enough together to even consider for one route (TODO: needs improvement).
# Once we have these clusters we can allow for additional flexibility in the overall solution by tweaking the segmentation determined by DBSCAN. Setting a fixed constraint of X miles might work initially, but there could be return routes, connecting stops, etc. that make one-offs more appealing.
# 
# #### using clusters to reduce node pools
# using dbscan we can select a chain-like cluster of nodes based on logic abstraction such as euclidean distance.

# In[ ]:


class DBSCAN:
    def __init__(self, x, y, epsilon=0.5, minpts=2, viz=None):
        self.epsilon = epsilon
        self.minpts = minpts
        self.viz = viz

    def to_dict(self):
        _dict = {'epsilon': self.epsilon, 'minpts': self.minpts}
        try:
            _dict['n X'] = len(self.X)
        except:
            logging.warning('X has not been set.')
        return _dict

    def fit(self, x, y):
        self.X = list(zip(x, y))
        self.clusters = np.zeros(len(self.X), dtype=np.int32)
        if self.viz:
            self.viz.x = x
            self.viz.y = y
            self.viz.update(self.clusters)

    @staticmethod
    def get_neighbors(X, i, epsilon):
        neighbors = []
        for j in range(0, len(X)):
            a = np.array(X[i])
            b = np.array(X[j])
            if np.linalg.norm(a-b) < epsilon:
                neighbors.append(j)
        return neighbors

    def build_cluster(self, i, neighbors, cluster):
        self.clusters[i] = cluster
        for j in neighbors:
            if self.clusters[j] == -1:
                self.clusters[j] = cluster
            elif self.clusters[j] == 0:
                self.clusters[j] = cluster
                points = self.get_neighbors(self.X, j, self.epsilon)
                if len(points) >= self.minpts:
                    neighbors += points

    def cluster(self, x=None, y=None):
        if x is None or y is None:
            X = self.X
        else:
            X = list(zip(x, y))

        cluster = 0
        for i in range(0, len(X)):
            if not self.clusters[i] == 0:
                continue
            points = self.get_neighbors(X, i, self.epsilon)
            if len(points) < self.minpts:
                self.clusters[i] = -1
            else:
                cluster += 1
                self.build_cluster(i, points, cluster)
            if self.viz:
                self.viz.update(self.clusters)

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

def test_add_closest_clusters():
    old_clusters = [1, 2, 3, None]
    new_clusters = add_closest_clusters([1, 2, 3, 4], [1, 2, 3, 4], old_clusters)
    
    assert len(old_clusters) == len(new_clusters)
    assert old_clusters != new_clusters
    assert new_clusters[-1] == 3 #hardcoded

def test_create_dbscan_basic():
    x, y = [1, 2, 3], [1, 2, 3]
    tdbscan = create_dbscan_basic(x, y)
    
    assert len(tdbscan.clusters) > 0
    assert len(tdbscan.clusters) == len(x)
    
def test_create_dbscan_expanded_clusters():
    x, y = [1, 2, 3], [1, 2, 3]
    clusters = create_dbscan_expanded_clusters(x, y)
    
    assert len(clusters) > 0
    assert len(clusters) == len(x)

test_add_closest_clusters()
test_create_dbscan_basic()
test_create_dbscan_expanded_clusters()

# simplify euclidean distance calculation by projecting to positive vals
x = df.latitude.values + 90
y = df.longitude.values + 180

# pyords cluster implementation
df['cluster'] = create_dbscan_expanded_clusters(x, y)
df.cluster = df.cluster.astype(str)
get_plot(df, 'cluster')


# ## Or-tools Modeling
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
class OrToolsTask:
    def __init__(self, manager, model):
        self.manager = manager
        self.model = model
        self.distances = None
        self.vehicles = None
        self.demand = None
        
    def distance_callback(self, i:int, j:int):
        """index of from (i) and to (j)"""
        node_i = self.manager.IndexToNode(i)
        node_j = self.manager.IndexToNode(j)

        return self.distances[node_i][node_j]
    
    def set_distance_callback(self):
        self.model.SetArcCostEvaluatorOfAllVehicles(
            self.model.RegisterTransitCallback(self.distance_callback)
        )
        
        return self
    
    def add_distances(self, distances):
        self.distances = distances
        self.set_distance_callback()
        
        return self
    
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
    
# constructing the model
def create_manager(n_nodes:int, n_vehicles:int, depot_index:int): 
    return pywrapcp.RoutingIndexManager(n_nodes, n_vehicles, 0)

def create_model(initialized_manager):
    return pywrapcp.RoutingModel(initialized_manager)

# config for optimization search
def create_search_params(max_solve_seconds:int=30):
    search_parameters = pywrapcp.DefaultRoutingSearchParameters()
    search_parameters.first_solution_strategy =         routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_parameters.time_limit.seconds = max_solve_seconds
    
    return search_parameters

# implementation
def create_origins_input():
    return [(41.4191, -87.7748)]
    
def create_distances_input(latitudes:list, longitudes:list):
    # TODO: abstraction & testing
    origins = create_origins_input() # assumed depot location for one-depot solutions
    distances = create_distances_matrix(origins, latitudes, longitudes)
    
    return distances

def create_vehicles_input(distances:list, m:int=26):
    # build vehicles of m cap by len(distances[1:])
    return [m for i in range(len(distances[1:]))] 

def create_demand_input(loads:np.array):
    # unit is load for each node with demand (in this case
    # only destinations). inserting 0 at the front of the array
    return np.insert(loads, 0, 0)
    
def solve_problem_w_ortools(distances:list, vehicles:list, demand:list):
    max_solve_seconds = 30
    depot_index = 0
    
    manager = create_manager(len(distances), len(vehicles), depot_index)
    model = create_model(manager)
    task = OrToolsTask(manager, model)
    search_params = create_search_params()
    assignment = task.add_distances(distances)        .add_vehicles(vehicles)        .add_demand(demand)        .run(search_params)
    
    return task.get_solution(assignment)

def init(dataframe:pd.DataFrame):
    lats, lons = dataframe.latitude, dataframe.longitude
    matrix = create_distances_input(lats, lons)
    vehicles = create_vehicles_input(matrix)
    demand = create_demand_input(dataframe.pallets.values)
    
    return matrix, vehicles, demand

def test_model_setup_implementation():
    lats, lons = [1, 2, 3], [1, 2, 3]
    origins = create_origins_input()
    matrix = create_distances_input(lats, lons)
    vehicles = create_vehicles_input(matrix)
    demand = create_demand_input([1, 2, 3])
    
    assert len(matrix) == len(origins) + len(lats)
    assert len(vehicles) == len(lats)
    assert len(demand) == len(matrix)

test_model_setup_implementation()

matrix, vehicles, demand = init(df)
basic_solution = solve_problem_w_ortools(matrix, vehicles, demand)

assert len(basic_solution) > 0 # TODO: create better solution testing

vehicleindex_w_moststops = np.argmax([len(v['stops']) for v in basic_solution])
vehicles_w_loads = [v for v in basic_solution if sum(v['stop_loads']) > 0]
print('test>> total vehicles: %s' % len(basic_solution))
print('test>> total vehicles w loads: %s' % len(vehicles_w_loads))
#print('total load: %s' % solution[-1])
#print('total input load: %s' % demand.sum())
print('test>> max stop sequence: %s' % basic_solution[vehicleindex_w_moststops]['stops'])


# ## Post-processing
# **Scoring** a solution against a standardized formula/method will allow for more comprehensive testing, debugging, and model tuning. Scoring should be broken down into a **theory score** and a **practical score**. Theory scores will utilize theoretical expectations of vrp solutions (some assumptions about implementations needs to be made). The practical score will measure how implementable a solution is with respect to certain real-world expectations.  
# 
# For the sake of simplicity I'll use pandas as my target format and align scoring to get functions that pull from standard solution structs.

# In[ ]:


class OrToolsChecks: # TODO: figure out best way to abstract checks & tests here
    def __init__(self, solution, dataframe:pd.DataFrame):
        self.solution = solution
        self.dataframe = dataframe
    
    # scoring theoretical
    # average capacity utilization of vehicles
    def get_load_factor(self, solution:list=None):
        if solution is None: solution = self.solution
            
        total_loads = sum([sum(s['stop_loads']) for s in solution])
        total_utilized_vehicles = len([s for s in solution if len(s['stops'][1:-1]) > 0])

        return total_loads / total_utilized_vehicles

    def score_load_factor(self, dataframe:pd.DataFrame=None):
        if dataframe is None: dataframe = self.dataframe
                
        return dataframe.groupby('vehicle').pallets.sum().mean()

    # average distance traveled per vehicle
    # NOTE: excluding distances returning to depot for now
    # need to refactor for this.
    def get_distance_factor(self, solution:list=None):
        if solution is None: solution = self.solution
            
        total_distances = sum([sum(s['stop_distances'][:-1]) for s in solution])
        total_vehicles = len([s for s in solution if len(s['stops'][1:-1]) > 0])

        return total_distances / total_vehicles

    def score_distance_factor(self, dataframe:pd.DataFrame=None):
        if dataframe is None: dataframe = self.dataframe
            
        return dataframe.groupby('vehicle').stop_distance.sum().mean()

    def get_travel_factor(self, solution:list=None):
        if solution is None: solution = self.solution
            
        total_distances = sum([sum(s['stop_distances'][:-1]) for s in solution])
        total_stops = sum([len(s['stops'][1:-1]) for s in solution])

        return total_distances / total_stops
    
    # average distance per stop
    def score_travel_factor(self, dataframe:pd.DataFrame=None):
        if dataframe is None: dataframe = self.dataframe
            
        return dataframe.stop_distance.mean()

    # ratio of one-stop routes to multi-stop 
    # (assumption is that implementation is looking for multi-stops)
    def get_multistop_factor(self, solution:list=None):
        if solution is None: solution = self.solution
        
        total_multistop_vehicles = len([s for s in solution if len(s['stops'][1:-1]) > 1])
        total_vehicles = len([s for s in solution if len(s['stops'][1:-1]) > 0])

        return total_multistop_vehicles / total_vehicles
        
    # general service measured in total capacity serviced over total in scope
    def score_multistop_factor(self, dataframe:pd.DataFrame=None):
        if dataframe is None: dataframe = self.dataframe
        vehicles = dataframe.groupby('vehicle')
        
        return (vehicles.size() > 1).sum() / len(vehicles)
    
    def get_satisfaction_factor(self, solution:list=None):
        if solution is None: solution = self.solution
        
        return None # TODO: can't pull from solution alone
    
    def score_satisfaction_factor(self, dataframe:pd.DataFrame=None):
        if dataframe is None: dataframe = self.dataframe
            
        return dataframe.stop_load.sum() / dataframe.pallets.sum()

    # scoring practice
    # deviation/distribution of stop distances per route
    def score_erratic_distance_factor(self, dataframe:pd.DataFrame=None):
        if dataframe is None: dataframe = self.dataframe
        
        return dataframe.stop_distance.std()

    # measuring total number of moves across state boarders
    def score_state_crossing_factor(self, dataframe:pd.DataFrame=None):
        if dataframe is None: dataframe = self.dataframe
            
        return None
    
    def get_df_info(self):
        return {
            'load_factor': self.score_load_factor(),
            'distance_factor': self.score_distance_factor(),
            'travel_factor': self.score_travel_factor(),
            'multistop_factor': self.score_multistop_factor(),
            'satisfaction_factor': self.score_satisfaction_factor(),
            'erratic_distance_factor': self.score_erratic_distance_factor(),
            'crossstate_factor': self.score_state_crossing_factor()
        }
    
    def psuedo_test(self):
        info = self.get_df_info()
        
        assert info['load_factor'] == self.get_load_factor()
        assert info['travel_factor'] == self.get_travel_factor()
        assert info['distance_factor'] == self.get_distance_factor()
        assert info['multistop_factor'] == self.get_multistop_factor()
        # NOTE: other factors are impossible to pull from just the solution
        # moving on for now.
        

def process_solution_to_dataframe(solution:list, dataframe:pd.DataFrame):
    for v in solution:
        # accounting for insert of origin to matrix input
        stops = list(np.array(v['stops'][1:-1]) - 1)

        dataframe.loc[stops, 'vehicle'] = str(v['vehicle'])
        dataframe.loc[stops, 'sequence'] = list(range(len(stops))) # assumes order matches
        dataframe.loc[stops, 'stop_distance'] = v['stop_distances'][1:-1]
        dataframe.loc[stops, 'stop_load'] = v['stop_loads'][1:-1]
    
    return dataframe        

basic_df = process_solution_to_dataframe(basic_solution, df)

checks = OrToolsChecks(basic_solution, df)
checks.psuedo_test()
print(checks.get_df_info())

get_plot(df, 'vehicle')


# ## Retry with DBSCAN

# In[ ]:


dbscan_df = df.copy()

results = pd.DataFrame(columns=dbscan_df.columns.tolist())

# TODO: optimize
for cluster in dbscan_df.cluster.unique():
    clustered_df = dbscan_df[dbscan_df.cluster == cluster].copy().reset_index(drop=True)
    
    matrix, vehicles, demand = init(clustered_df)
    solution = solve_problem_w_ortools(matrix, vehicles, demand)
    clustered_df = process_solution_to_dataframe(solution, clustered_df)
    clustered_df.vehicle = str(int(cluster)) + '-' + clustered_df.vehicle.astype(int)        .astype(str)
    results = results.append(clustered_df, sort=False)

results.pallets = results.pallets.astype(int)
    
dbscan_df = results
dbscan_checks = OrToolsChecks(solution=None, dataframe=dbscan_df)
print(dbscan_checks.get_df_info())
get_plot(dbscan_df, 'vehicle')


# In[ ]:


checks.get_df_info()


# In[ ]:


dbscan_checks.get_df_info()

