from .algorithm import GeneticAlgorithm

class DedicatedFleetGA(GeneticAlgorithm):
    '''
    Purpose:
        Provide a genetic algorithm for routing a dedicated fleet to a set
        of nodes with demand. This algorithm takes into account several
        constraints: demand, capacity, and time windows. For the first phase
        of these models, shipment data will be preprocessed to decompose the
        problem, identifying ideal routes to solve. Clustering for these routes
        may reduce runtime.
    '''
    def __init__(self, distances:np.array, routes:np.array, windows:np.array, demands:np.array,
    vehicles:np.array, ):
        '''
        Args:
            distances: matrix of all-to-all distances (defines order).
            routes: matrix of all-to-all route mapping. All-to-all segments are
            pre-mapped to a given route.
            times: array of time windows for each location (follows order).
            demands: array of demands for each location.
            vehicles: array of capacities representing a vehicle.
        '''
        GeneticAlgorithm.__init__(self)
        self.distances = distances
        self.routes = routes
        self.windows = windows
        self.demands = demands
        self.vehicles = vehicles

    def fitness(self):
        pass
