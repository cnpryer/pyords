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

    def initialize_population(self, individual:np.array,
    population:np.array=None):
        '''
        Purpose:
            Initilizes model with population of individuals. If an individual
            is passed, the algorithm will see this as a trigger to randomly
            produce more individuals.

        Args:
            individual: a sample individual to use
            population: a warm-start population to use instead of randomized.
            this can also serve as the pool from which randomized individuals
            are created.
        '''
        pass

    def repoduce(self, population:np.array):
        '''
        Purpose:
            Produces new population

        Args:
            population: array of individuals for reproduction.
        '''
        pass

    def evolve(self):
        '''manages genetic algorithm'''
        pass
