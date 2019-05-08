import numpy as np
from .base import GeneticAlgorithm

class DedicatedFleetGA(GeneticAlgorithm):
    '''
    Purpose:
        Provide a genetic algorithm for routing a dedicated fleet to a set
        of nodes with demand. This algorithm takes into account several
        constraints: demand, capacity, and time windows. For the first phase
        of these models, shipment data will be preprocessed to decompose the
        problem, identifying ideal routes to solve. Clustering for these routes
        may reduce runtime. For this first pass the design of this code will be
        simplified.

    TODO:
        The idea is to initialize genetic algorithms with agnostic structures
        that have values used to map back to the data to optimize or simulate.
    '''
    def __init__(self, distances:np.array, routes:np.array, windows:np.array,
    demands:np.array, vehicles:np.array, settings:dict):
        '''
        Args:
            distances: matrix of all-to-all distances (defines order).
            routes: matrix of from-origin route mapping. A subest of all-to-all
            segments are pre-mapped to a given route by their indexes in
            distances ([[0, 2, 5, 3, 0], ...]).
            times: array of time windows for each location (follows order).
            demands: array of demands for each location.
            vehicles: array of capacities representing a vehicle.
        '''
        GeneticAlgorithm.__init__(self, settings)
        self.distances = distances
        self.routes = routes
        self.windows = windows
        self.demands = demands
        self.vehicles = vehicles
        self.penalties = settings['penalties']

    def encode(self):
        '''
        Purpose:
            Encode routes as a list of individuals that represent a set of
            routes with randomized or clustered stops not including origin.
            Dedicated models assume return to origin is required. For random
            individuals the following example occurs:
                i1 = [[1, 2, 3], [4, 5, 6, 7], []]
            where individual i1 has two routes that hit both a different number
            of stops and the stops on each route differ.
        '''
        pass

    def fitness(self):
        '''
        Purpose:
            Assess the performance of each evolution of the solution
        '''
        pass

    def run(self):
        '''manages algorithm'''
        population = self.initialize(self.routes)
