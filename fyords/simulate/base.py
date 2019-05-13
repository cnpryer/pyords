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
            # TODO: determind diveristy
            #replace=False,
            p=self.selection_probabilities
        )

    def crossover(self, population:np.array):
        '''
        Purpose:
            Basic genetic crossover. First pass version will crossover in
            pairs over the length of the population.

        population: population: array of individuals for reproduction
        sorted by fitness.
        '''
        cross = np.random.random(self.population_size) < self.crossover_rate
        new = list(population[np.invert(cross)].copy())
        #print(len(population[cross]))
        n = population[cross].size # n pairs
        # TODO: might want to retain ordering by fitness evaluation
        # this would leave the remainder (not crossed pairwise) as the least
        # ideal individual.
        for second in range(1, n, 2):
            for child in range(0, 2):
                # TODO: probably increasing genetic material
                A = population[cross][second-1]
                Ai = np.random.randint(0, A.size)
                B = population[cross][second]
                Bi = np.random.randint(0, B.size)
                Ac = list(A[:Ai])
                Bc = list(B[:Bi])
                C = Ac + Bc
                if len(C) == 1:
                    C += C
                elif len(C) == 0:
                    C = [A, B][np.random.randint(0, 1)]
                new.append(C)
        if n % 2 != 0:
            new.append(list(population[cross])[-1])
        return np.array(new)

    def mutation(self, population:np.array):
        '''
        Puropse:
            Randomized mutation of genetic material. To remain abstracted,
            this function should randimize the properties of each element of
            an individual. For the first pass it will just shuffle an
            individuals elements.
        '''
        mutate = np.random.random(self.population_size) < self.mutation_rate
        new = list(population[np.invert(mutate)])
        new += [np.random.shuffle(i) for i in population[mutate]]
        return np.array(mutate)

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
        population = self.selection(population)
        population = self.crossover(population)
        population = self.mutation(population)
        return population
