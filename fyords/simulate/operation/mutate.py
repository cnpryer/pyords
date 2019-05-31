import numpy as np

class MutationBase:
    def __init__(self):
        pass

class SimpleMutation(MutationBase):
    def __init__(self, rate=0.01):
        MutationBase.__init__(self)
        self.rate = rate

    def set_mutate(self, population):
        n = len(population)
        self.mutate_bools = np.random.random(n) < self.rate
        self.mutate = [population[i] for i, y
                       in enumerate(self.mutate_bools) if y]

    def run(self, population):
        self.set_mutate(population)
        new = [population[i] for i, y in enumerate(self.mutate_bools) if not y]
        new += [np.random.shuffle(i) for i in self.mutate]
        return new
