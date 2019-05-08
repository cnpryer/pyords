import numpy as np
import random

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

    def initialize(self):
        '''
        TODO:
            Need to define agnostic initialization.
        '''
        return None

    def reproduce(self, population:np.array):
        '''
        Purpose:
            Produces new population

        Args:
            population: array of individuals for reproduction.
        '''
        pass
