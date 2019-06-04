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
        """Assumes highest to lowest index ordering of population"""
        self.probabilities = [weight/sum(weights) for weight in weights]

    def run(self, population):
        n = len(population)
        self.set_weights(n)
        self.set_probabilities(self.weights)
        indices = np.arange(n)
        selected = np.random.choice(
            indices,
            size=n,
            # TODO: determine diversity
            #replace=False,
            p=self.probabilities)
        return [population[i] for i in selected]
