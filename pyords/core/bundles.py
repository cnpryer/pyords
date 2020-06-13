from ortools.constraint_solver import routing_enums_pb2
from ortools.constraint_solver import pywrapcp

import pandas as pd
import numpy as np


class VrpBundle:

    def __init__(self, matrix:list=None, demand:list=None, case=None):
        """
        light cascader - give input -> init -> run ... tweak?
        matrix: [[list] of lists ...] defining nodes by position 
        and a distance from every other node (assumes origin is included @ 0).
        vehicles: [max_caps for ... n vehicles]
        TODO: case: pyords test Case obj
        """
        self.matrix = matrix
        self.demand = demand

        if case:
            return self.initialize_case(case)

        self.vehicles = self.create_vehicles()
        self.ortools()

        return None

    def create_vehicles(self, max_capacity:int=26):
        """
        assumes origin is position 0 in self.matrix and
        defines a vehicle of max_cap for each destination.
        """
        return [max_capacity for i in range(len(self.matrix[1:]))] 
        
    def create_manager(self):
        return pywrapcp.RoutingIndexManager(len(self.matrix), len(self.vehicles), 0)

    def matrix_callback(self, i:int, j:int):
        """index of from (i) and to (j)"""
        node_i = self.manager.IndexToNode(i)
        node_j = self.manager.IndexToNode(j)

        return self.matrix[node_i][node_j]

    def demand_callback(self, i:int):
        """capacity constraint"""
        node = self.manager.IndexToNode(i)

        return self.demand[node]

    def create_model(self):
        model = pywrapcp.RoutingModel(self.manager)

        # distance constraint setup
        model.SetArcCostEvaluatorOfAllVehicles(
            model.RegisterTransitCallback(self.matrix_callback)
        )

        # demand constraint setup
        model.AddDimensionWithVehicleCapacity(
            # function which return the load at each location (cf. cvrp.py example)
            model.RegisterUnaryTransitCallback(self.demand_callback),
            0, # null capacity slack
            np.array([cap for cap in self.vehicles]), # vehicle maximum capacity
            True, # start cumul to zero
            'Capacity'
        )

        return model

    def create_search_params(self, max_seconds=30):
        search_parameters = pywrapcp.DefaultRoutingSearchParameters()
        search_parameters.first_solution_strategy = \
            routing_enums_pb2.FirstSolutionStrategy.PATH_CHEAPEST_ARC
        search_parameters.time_limit.seconds = max_seconds
        
        return search_parameters

    def get_solution(self):
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
                i = self.assignment.Value(self.model.NextVar(i))
                info['stop_distances'].append(self.model.GetArcCostForVehicle(previous_i, i, vehicle))

            # add return to depot to align with solution data
            info['stops'].append(0)
            info['stop_loads'].append(0)
            solution.append(info)
        
        return solution

    def ortools(self):
        """init of ortools modeling"""
        self.manager = self.create_manager()
        self.model = self.create_model()

        return self

    def run(self, max_search_seconds:int=30):
        search = self.create_search_params(max_search_seconds)
        self.assignment = self.model.SolveWithParameters(search)

        return self
    
    def cast_solution_to_df(self, dataframe:pd.DataFrame):
        """assumes data positions match"""
        for v in self.get_solution():
            # accounting for insert of origin to matrix input
            stops = list(np.array(v['stops'][1:-1]) - 1)

            dataframe.loc[stops, 'vehicle'] = str(v['vehicle'])
            dataframe.loc[stops, 'sequence'] = list(range(len(stops))) # assumes order matches
            dataframe.loc[stops, 'stop_distance'] = v['stop_distances'][1:-1]
            dataframe.loc[stops, 'stop_load'] = v['stop_loads'][1:-1]
        
        return dataframe

    def initialize_case(self, case):
        n_dest_nodes = len(case.inputs['matrix'][1:])
        self.matrix = case.inputs['matrix']
        self.vehicles = [case.inputs['max_vehicle_capacity'] for i in range(n_dest_nodes)]
        self.demand = case.inputs['demand']

        self.case = case

        return None

    def test(self):
        self.ortools()
        bndl = self.run(self.case.inputs['max_search_seconds'])
        solution = bndl.get_solution()
        
        assert len(solution) == len(self.vehicles)

        return solution is not None
    