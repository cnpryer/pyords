from ..evaluation import SimpleFitness
from ..operation import (
    SimpleSelection,
    SimpleCrossover,
    SimpleMutation
)
from . import (
    SimpleIndividual,
    VariedSizeIndividual,
    SimpleInitialization)
import numpy as np
import pandas as pd

class PopulationBase:
    def __init__(self):
        pass

class GeneticPopulation(PopulationBase):
    def __init__(self,
                initialization=None,
                population=None,
                fitness=None,
                selection=None,
                crossover=None,
                mutation=None,
                generations=100):
        """
        Population class for Genetic Algorithm.
        Args:
            initialization: fyords.initialization object to define
            initialization of population data.
            population: array of fyords.population.individuals to use as
            population data (TODO: does this replace initialization?).
            fitness: fyords.evaluate.fitness used to evaluate individuals.
            selection: fyords.operation.selection to use for identifying
            potential crossover pairs.
            crossover: fyords.operation.crossover to use for swapping elements
            of selected pairs.
            mutation: fyords.operation.mutation to use for mutating elements of
            individuals.
            generations: number of generations of population simulation.
        """
        PopulationBase.__init__(self)
        self.fitness = \
            SimpleFitness() if fitness is None else fitness
        self.population = [] if population is None else population
        # TODO: SimpleInitialization().run() if population is None else population
        self.selection = \
            SimpleSelection() if selection is None else selection
        self.crossover = \
            SimpleCrossover() if crossover is None else crossover
        self.mutation = \
            SimpleMutation() if mutation is None else mutation

    def run(self):
        scores = \
            [self.fitness.run(individual) for individual in self.population]
        order = np.argsort(scores)
        self.population = self.population[order]
        self.population = self.selection.run(self.population)
        self.population = self.crossover.run(self.population)
        self.population = self.mutation.run(self.population)
        return self.population
