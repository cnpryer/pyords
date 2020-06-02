import logging
import sys
import numpy as np

class BasicGeneticAlgorithm:
    def __init__(self, first_individual, environment, fitness_func,
        population_size=10, n_generations=100, selection_depreciation=0.5,
        crossover_rate=0.7, crossover_percent=0.5, mutation_rate=0.05,
        viz=None):
        """Returns optimized solution based off initial individual and fitness
        function."""
        self.first_individual = first_individual
        self.environment = environment
        self.n_generations = n_generations
        self.population = self.initialize_population(
            first_individual, population_size)
        self.fitness_func = fitness_func
        self.population_size = population_size
        self.selection_depreciation = selection_depreciation
        self.crossover_rate = crossover_rate
        self.crossover_percent = crossover_percent
        self.mutation_rate = mutation_rate
        self.viz = viz

    def to_dict(self):
        return {
            'first_individual_len': len(self.first_individual),
            'n_generations': self.n_generations,
            'population_size': self.population_size,
            'selection_depreciation': self.selection_depreciation,
            'crossover_rate': self.crossover_rate,
            'crossover_percent': self.crossover_percent,
            'mutation_rate': self.mutation_rate
        }

    def initialize_population(self, first_individual, size):
        """Initializes a population from the set of chromosomes from the first
        individual"""
        pool = first_individual
        return np.random.choice(pool, (size, len(pool)))

    def evaluate(self):
        scores = [-self.fitness_func(individual, self.environment)
            for individual in self.population]
        if self.viz:
            self.viz.update(max(scores))
        ranking = np.argsort(scores)
        return [self.population[i] for i in ranking]

    def select(self):
        new_population = self.evaluate()
        reverse = np.arange(self.population_size, 0, -1)
        weights = np.power(reverse, self.selection_depreciation)
        probabilities = [weight/sum(weights) for weight in weights]
        pool = np.arange(self.population_size)
        selected = np.random.choice(pool, size=self.population_size,
            p=probabilities)
        self.population = np.array([new_population[i] for i in selected])

    def crossover(self):
        n = len(self.first_individual)
        new_population = self.population.copy()
        split = (int(self.population_size/2))
        indicies = np.random.randint(0, n, size=split)
        for i, start in np.ndenumerate(indicies):
            index = i[0] * 2
            end = start + int((n*self.crossover_percent))
            new_population[index, start:end] = \
                self.population[index+1, start:end]
            new_population[index+1, start:end] = \
                self.population[index, start:end]
        chances = np.random.random(size=self.population_size)
        ignore = chances > self.crossover_rate
        new_population[ignore] = self.population[ignore]
        self.population = new_population

    def mutate(self):
        n = len(self.first_individual)
        chances = np.random.random(size=self.population.shape)
        indicies = chances < self.mutation_rate
        impact = indicies.sum()
        self.population[indicies] = np.random.randint(0, n, size=impact)

    def run(self):
        logging.info('GA initiated with : %s' % self.to_dict())
        for i in range(self.n_generations):
            logging.info('Running generation %s' % i)
            self.select()
            self.crossover()
            self.mutate()
        return self.evaluate()[0]
