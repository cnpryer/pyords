from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import logging

def ovrp_to_df(df, solution):
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


class GoogleORCVRP:
    def __init__(self, distances, demand, vehicles, depot, max_seconds):
        self.distances = distances
        self.n_nodes = len(distances)
        self.demand = demand
        self.vehicle_min_capacities = np.array([i[0] for i in vehicles])
        self.vehicle_max_capacities = np.array([i[1] for i in vehicles])
        self.n_vehicles = len(vehicles)
        self.depot = depot
        self.max_seconds = max_seconds
        self.solution = []

    def to_dict(self):
        return {
            'n nodes': self.n_nodes,
            'total demand': self.demand.sum(),
            'average demand': self.demand.mean(),
            'n vehicles': self.n_vehicles,
            'average vehicle capacity': self.vehicle_max_capacities.mean(),
            'depot': self.depot,
            'max seconds': self.max_seconds,
            'solved': len(self.solution) > 0
        }

    def save_solution(self):
        total_distance = 0
        total_load = 0
        for vehicle in range(self.n_vehicles):
            i = self.model.Start(vehicle)
            info = {'vehicle': vehicle, 'route': '', 'stops': set()}
            route_distance = 0
            route_load = 0
            while not self.model.IsEnd(i):
                node = self.manager.IndexToNode(i)
                route_load += self.demand[node]
                info['route'] += ' {0} Load({1})'.format(node, route_load)
                previous_i = i
                i = self.assignment.Value(self.model.NextVar(i))
                route_distance += self.model.GetArcCostForVehicle(
                    previous_i, i, vehicle)
                info['stops'].add(node)
            info['route'] += ' {0} Load({1})'.format(
                self.manager.IndexToNode(i), route_load)
            info['route'] = info['route'][1:] # strip leading zero
            info['dist'] = route_distance
            info['load'] = route_load
            self.solution.append(info)
            total_distance += route_distance
            total_load += route_load
        self.solution.append({'total dist': total_distance})
        self.solution.append({'total load': total_load})

    def distance_callback(self, i, j):
        """index of from (i) and to (j)"""
        node_i = self.manager.IndexToNode(i)
        node_j = self.manager.IndexToNode(j)
        return self.distances[node_i][node_j]

    def demand_callback(self, i):
        """capacity constraint"""
        node = self.manager.IndexToNode(i)
        return self.demand[node]

    def set_manager(self):
        self.manager = pywrapcp.RoutingIndexManager(
            self.n_nodes, self.n_vehicles, self.depot)

    def set_model(self):
        self.model = pywrapcp.RoutingModel(self.manager)
        transit_callback_index = \
            self.model.RegisterTransitCallback(self.distance_callback)
        self.model.SetArcCostEvaluatorOfAllVehicles(transit_callback_index)
        demand_callback_index = \
            self.model.RegisterUnaryTransitCallback(self.demand_callback)

        # null capacity slack (arg: 0); start cumul to zero (arg: True)
        self.model.AddDimensionWithVehicleCapacity(
            demand_callback_index, # function which return the load at each location (cf. cvrp.py example)
            0, # null capacity slack
            self.vehicle_max_capacities, # vehicle maximum capacity
            True, # start cumul to zero
            'Capacity')
        capacity_dimension = self.model.GetDimensionOrDie('Capacity')
        for i, n in enumerate(self.vehicle_min_capacities):
            capacity_dimension.CumulVar(self.model.End(i)).RemoveInterval(0, int(n))
        
    def set_search_params(self):
        self.search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        self.search_parameters.first_solution_strategy = \
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        self.search_parameters.time_limit.seconds = self.max_seconds

    def solve(self):
        self.set_manager()
        self.set_model()
        self.set_search_params()
        self.assignment = \
            self.model.SolveWithParameters(self.search_parameters)
        if self.assignment:
            self.save_solution()
