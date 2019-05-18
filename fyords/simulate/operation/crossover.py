import numpy as np

class CrossoverBase:
    def __init__(self):
        pass

class SimpleCrossover(CrossoverBase):
    def __init__(self, rate=0.7):
        CrossoverBase.__init__(self)
        self.rate = rate

    def set_cross(self, population_size):
        self.cross = np.random.random(population_size) < self.rate

    def run(self, population):
        n = len(population)
        self.set_cross(n)
        new = list(population[np.invert(self.cross)].copy())
        #print(len(population[cross]))
        n = population[self.cross].shape[0] # n pairs
        # TODO: might want to retain ordering by fitness evaluation
        # this would leave the remainder (not crossed pairwise) as the least
        # ideal individual.
        for second in range(1, n, 2):
            for child in range(0, 2):
                # TODO: probably increasing genetic material
                A = population[self.cross][second-1]
                Ai = np.random.randint(0, A.shape[0])
                B = population[self.cross][second]
                Bi = np.random.randint(0, B.shape[0])
                Ac = list(A[:Ai])
                Bc = list(B[:Bi])
                C = Ac + Bc
                if len(C) == 1:
                    C += C
                elif len(C) == 0:
                    C = [A, B][np.random.randint(0, 1)]
                new.append(C)
        if n % 2 != 0:
            new.append(list(population[self.cross])[-1])
        return np.array(new)
