import numpy as np

class CrossoverBase:
    def __init__(self):
        pass

class SimpleCrossover(CrossoverBase):
    def __init__(self, rate=0.7):
        CrossoverBase.__init__(self)
        self.rate = rate

    def set_cross(self, population):
        n = len(population)
        self.cross_bools = np.random.random(n) < self.rate
        self.cross = [population[i] for i, y
                      in enumerate(self.cross_bools) if y]

    def run(self, population):
        self.set_cross(population)
        new = [population[i] for i, y
               in enumerate(self.cross_bools) if not y]
        n = len(self.cross)
        for second in range(1, n, 2):
            for child in range(0, 2):
                # TODO: (needs work)
                #  Probably increasing genetic material.
                #  Also need to properly handle empty children, unless this
                #  becomes illegal.
                A = self.cross[second-1]
                An = 1
                if A is not None:
                    An = len(A)
                Ai = np.random.randint(0, An)
                B = self.cross[second]
                Bn = 1
                if B is not None:
                    Bn = len(B)
                Bi = np.random.randint(0, Bn)
                Ac = A[:Ai]
                Bc = B[:Bi]
                C = Ac + Bc
                if len(C) == 1:
                    C += C
                elif len(C) == 0:
                    C = [A, B][np.random.randint(0, 1)]
                new.append(C)
        if n % 2 != 0:
            new.append(self.cross[-1])
        return new
