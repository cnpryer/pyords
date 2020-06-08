from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
from ..distance.matrix import ovrp_haversine_distance_matrix
import pandas as pd
import numpy as np

import logging


def ovrp_to_df(df:pd.DataFrame, solution:list): # TODO: do something with this
    """Assuming df row positions lines up with the input to the Google OR
    model - 1 (ovrp begins with a fake node), apply a shipment_id to the
    dataframe."""
    shipment_id = np.zeros(len(df), dtype=np.int32) - 1
    vehicles = [obj for obj in solution if 'vehicle' in list(obj)]
    for i, vehicle in enumerate(vehicles):
        stops = np.array([n for n in list(vehicle['stops']) if n > 0])
        nodes = stops - 1
        if len(nodes) > 0:
            shipment_id[nodes] = i

    return shipment_id

def get_manager_basic(distances:list, vehicles:list, depot_index:int):
    return pywrapcp.RoutingIndexManager(len(distances), len(vehicles), depot_index)

def get_search_config_basic(max_solve_seconds:int):
    search_params = pywrapcp.DefaultRoutingSearchParameters()
    search_params.first_solution_strategy = routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
    search_params.time_limit.seconds = max_solve_seconds
    
    return search_params

class OrtoolsCvrpDataFrame:
    def __init__(self, df:pd.DataFrame, depot_index:int=0, max_solve_seconds:int=30):
        self.df = df
        self.depot_index = depot_index
        self.max_solve_seconds = max_solve_seconds

        self.distances = ovrp_haversine_distance_matrix(
            lats=df.latitude.values,
            lons=df.longitude.values,
            unit='mi'
        )
        self.demand = np.insert(df.pallets.values, 0, 0)
        self.vehicles = [26]*len(self.distances) # TODO: abstract this

    def set_max_solve_seconds(self, seconds:int=30):
        self.max_solve_seconds = seconds
    
    def set_depot_index(self, index:int=0):
        self.depot_index = index

    def to_dict(self):
        logging.warning('this function needs to be updated for v0.0.4 refactor')
        
        return {
            'n nodes': None,
            'total demand': None,
            'average demand': None,
            'n vehicles': None,
            'average vehicle capacity': None,
            'depot': None,
            'max seconds': None,
            'solved': None > 0
        }

    def get_solution(self, result, model:pywrapcp.RoutingModel):
        total_distance = 0
        total_load = 0
        solution = []
        for vehicle in range(len(self.vehicles)):
            i = model.Start(vehicle)
            info = {'vehicle': vehicle, 'route': '', 'stops': set()}
            route_distance = 0
            route_load = 0
            while not model.IsEnd(i):
                node = self.manager.IndexToNode(i)
                route_load += self.demand[node]
                info['route'] += ' {0} Load({1})'.format(node, route_load)
                previous_i = i
                i = result.Value(model.NextVar(i))
                route_distance += model.GetArcCostForVehicle(
                    previous_i, i, vehicle)
                info['stops'].add(node)
            info['route'] += ' {0} Load({1})'.format(
                self.manager.IndexToNode(i), route_load)
            info['route'] = info['route'][1:] # strip leading zero
            info['dist'] = route_distance
            info['load'] = route_load
            solution.append(info)
            total_distance += route_distance
            total_load += route_load
    
        return solution
    
    def distance_callback_basic(self, i:int, j:int):
        """index of from (i) and to (j)"""
        node_i = self.manager.IndexToNode(i)
        node_j = self.manager.IndexToNode(j)

        return self.distances[node_i][node_j]

    def demand_callback_basic(self, i:int):
        """capacity constraint"""
        node = self.manager.IndexToNode(i)

        return self.demand[node]

    def get_model(self, manager:pywrapcp.RoutingIndexManager, distance_func, demand_func):
        model = pywrapcp.RoutingModel(manager)
        transit_callback_index = model.RegisterTransitCallback(distance_func)
        model.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)

        demand_callback_index = model.RegisterUnaryTransitCallback(demand_func)

        # null capacity slack (arg: 0); start cumul to zero (arg: True)
        model.AddDimensionWithVehicleCapacity(
            demand_callback_index, # function which return the load at each location (cf. cvrp.py example)
            0, # null capacity slack
            np.array([cap for cap in self.vehicles]), # vehicle maximum capacity
            True, # start cumul to zero
            'Capacity'
        )
        #capacity_dimension = self.model.GetDimensionOrDie('Capacity')
        #for i, n in enumerate(self.vehicle_min_capacities):
        #    capacity_dimension.CumulVar(self.model.End(i)).RemoveInterval(0, int(n))

        return model

    def solve(self):
        self.manager = get_manager_basic(self.distances, self.vehicles, self.depot_index)
        search_config = get_search_config_basic(self.max_solve_seconds)
        model = self.get_model(
            self.manager,
            distance_func=self.distance_callback_basic,
            demand_func=self.demand_callback_basic    
        )
        result = model.SolveWithParameters(search_config)

        if result:
            solution = self.get_solution(result, model)
            output_vehicles = solution[:-2] # TODO: fix this
            vehicleindex_w_moststops = np.argmax([len(v['stops']) for v in output_vehicles])
            vehicles_w_loads = [v for v in output_vehicles if v['load'] > 0]

            logging.debug('total vehicles: %s' % len(output_vehicles))
            logging.debug('total vehicles w loads: %s' % len(vehicles_w_loads))
            logging.debug('total load: %s' % solution[-1])
            logging.debug('total input load: %s' % self.df.pallets.sum())
            logging.debug('max stop sequence: %s' % output_vehicles[vehicleindex_w_moststops]['stops'])
            
            for vehicle in vehicles_w_loads:
                locs = np.array(list(vehicle['stops'])[1:]) - 1
                self.df.loc[locs, 'vehicle'] = vehicle['vehicle']