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
            Need to define agnostic initialization. As of now *initialization*
            is pooled into the encoding of the problem, where encoding refers to
            the creation of individuals by seeding techniques (random or
            clustered). This is currently a preproccesing step.
        '''
        pass

    def reproduce(self, population:np.array):
        '''
        Purpose:
            Produces new population by selecting individuals to reproduce,
            reproducing via crossover of their genetic material, and randomly
            applying mutation.

        Args:
            population: array of individuals for reproduction sorted by fitness.
        '''
        def selection():
            '''fitness-based lottery utilizing pre-sorted population'''
            pass

        def crossover():
            '''basic genetic crossover'''
            pass

        def mutation():
            '''randomized mutation of genetic material'''
            pass
            
        pass
