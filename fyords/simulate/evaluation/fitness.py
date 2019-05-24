class FitnessBase:
    def __init__(self):
        pass

class SimpleFitness(FitnessBase):
    def __init__(self, function, constants):
        FitnessBase.__init__(self)
        self.function = function
        self.constants = constants

    def run(self, individual):
        return self.function(individual, self.constants)
