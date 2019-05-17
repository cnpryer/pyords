import numpy as np

class MutationBase:
    def __init__(self):
        pass

class SimpleMutation(MutationBase):
    def __init__(self, rate=0.01):
        MutationBase.__init__(self)
        self.rate = rate

    def set_mutate(self, population_size):
        self.mutate = \
            np.random.random(population_size) < self.rate

    def run(self, population):
        n = len(population)
        self.set_mutate(n)
        new = list(population[np.invert(self.mutate)])
        new += [np.random.shuffle(i) for i in population[self.mutate]]
        return np.array(new) # TODO: this used 'mutate', test 'new'
