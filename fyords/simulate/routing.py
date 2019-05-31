import numpy as np

class DedicatedFleetGA(GeneticAlgorithm):
    """Provide a genetic algorithm for routing a dedicated fleet to a set
    of nodes with demand. This algorithm takes into account several
    constraints: demand, capacity, and time windows. For the first phase
    of these models, shipment data will be preprocessed to decompose the
    problem, identifying ideal routes to solve. Clustering for these routes
    may reduce runtime. For this first pass the design of this code will be
    simplified.

    Encoding is done as a preprocessing step. Encode routes as a list of
    individuals where each represents a set of routes with randomized stops
    not including origin. Dedicated models assume return to origin is
    required. For random individuals the following encoding is expected:
        i1 = [[1, 2, 3], [4, 5, 6, 7], []]
    where individual i1 has two routes that hit both a different number
    of stops and the stops between each route differ.

    TODO:
        The idea is to initialize genetic algorithms with agnostic structures
        that have values used to map back to the data to optimize or simulate.
        Beyond the initial design the goal is to abstract objects such as
        individual, population, etc.
    """
    def __init__(self, distances: np.array, routes: np.array,
                 windows: np.array, demands: np.array, vehicles: np.array,
                 settings: dict):
        """
        Parameters
        ----------
        distances: matrix of all-to-all distances (defines order).
        routes: encoded population containing sets of routes that
        represent an individual
        distances ([[0, 2, 5, 3, 0], ...]).
        times: array of time windows for each location (follows order).
        demands: array of demands for each location.
        vehicles: array of capacities representing a vehicle.
        """
        GeneticAlgorithm.__init__(self, settings)
        self.distances = distances
        self.routes = routes
        self.windows = windows
        self.demands = demands
        self.vehicles = vehicles
        self.penalties = settings['penalties']