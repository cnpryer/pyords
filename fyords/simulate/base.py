import numpy as np

class GeneticAlgorithm:
    '''
    Purpose:
        Base code for genetic algorithms.
    '''
    def __init__(self, settings:dict):
        self.generations = settings['generations']
        self.population_size = settings['population_size']
        self.crossover_rate = settings['crossover_rate']
        self.mutation_rate = settings['mutation_rate']
        self.individual_size = settings['individual_size']

    def initialize(self, population:np.array=None):
        '''
        Purpose:
            Initilizes model with population of randomized individuals
            using preprocessed population. Eventually this will allow
            warm-starts.

        Args:
            population: a preprocessed first population to randomize.

        TODO:
            The randomization needs to be model-specific.
        '''
        return None


    def repoduce(self, population:np.array):
        '''
        Purpose:
            Produces new population

        Args:
            population: array of individuals for reproduction.
        '''
        pass
