import numpy as np

class MutationBase:
    def __init__(self):
        pass

class SimpleMutation(MutationBase):
    def __init__(self, rate=0.05):
        MutationBase.__init__(self)
        self.rate = rate

    def set_mutate(self, population):
        n = len(population)
        self.mutate_bools = np.random.random(n) < self.rate
        self.mutate = [population[i] for i, y
                       in enumerate(self.mutate_bools)
                       if y and population[i] is not None]

    def run(self, population):
        self.set_mutate(population)
        new = [population[i] for i, y in enumerate(self.mutate_bools)
               if not y or population[i] is None]
        for individual in self.mutate:
            for element in individual:
                np.random.shuffle(np.array(element))
        new += self.mutate
        return new
