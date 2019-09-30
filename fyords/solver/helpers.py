from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp
import numpy as np
import logging

class GoogleORCVRP:
    def __init__(self, distances, demand, vehicles, depot, max_seconds):
        self.distances = distances
        self.n_nodes = len(distances)
        self.demand = demand
        self.vehicles = np.array(vehicles)
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
            'average vehicle capacity': self.vehicles.mean(),
            'depot': self.depot,
            'max seconds': self.max_seconds,
            'solved': len(self.solution) > 0
        }

    def save_solution(self):
        total_distance = 0
        total_load = 0
        for vehicle in range(self.n_vehicles):
            i = self.model.Start(vehicle)
            info = {'vehicle': vehicle, 'route': ''}
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
            demand_callback_index, 0, self.vehicles, True, 'Capacity')

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
