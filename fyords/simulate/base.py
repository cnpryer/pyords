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
        # TODO: figure out why **0.5 doesn't sum to 1.
        # probability weights
        w = np.power(np.arange(settings['population_size'], 0, -1), 0.5)
        # probability percent to use as selection bias
        self.selection_probabilities = w / w.sum()
        self.crossover_rate = settings['crossover_rate']
        self.mutation_rate = settings['mutation_rate']

    def selection(self, population:np.array):
        '''
        Prupose:
            Fitness-based lottery utilizing pre-sorted population

        Args:
            population: population: array of individuals for reproduction
            sorted by fitness.
        '''
        return np.random.choice(
            population,
            size=self.population_size,
            replace=False,
            p=self.selection_probabilities
        )

    def crossover(self):
        '''basic genetic crossover'''
        pass

    def mutation(self):
        '''randomized mutation of genetic material'''
        pass

    def reproduce(self, population:np.array):
        '''
        Purpose:
            Produces new population by selecting individuals to reproduce,
            reproducing via crossover of their genetic material, and randomly
            applying mutation. These functions as of now are abstracted for
            testing & development.

        Args:
            population: array of individuals for reproduction sorted by fitness.
        '''
        pass
