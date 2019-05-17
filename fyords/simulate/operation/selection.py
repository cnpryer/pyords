import numpy as np

class SelectionBase:
    def __init__(self):
        pass

class SimpleSelection(SelectionBase):
    def __init__(self, depreciation=0.5):
        SelectionBase.__init__(self)
        self.depreciation = depreciation

    def set_weights(self, population_size):
        self.weights = \
            np.power(np.arange(population_size, 0, -1), self.depreciation)

    def set_probabilities(self, weights):
        '''assumes highest to lowest index ordering of population'''
        self.probabilities = weights / weights.sum()

    def run(self, population):
        n = len(population)
        self.set_weights(n)
        self.set_probabilities(self.weights)
        return np.random.choice(
            population,
            size=n,
            # TODO: determind diveristy
            #replace=False,
            p=self.probabilities)
