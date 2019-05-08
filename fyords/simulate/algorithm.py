class GeneticAlgorithm:
    '''
    Purpose:
        Base code for genetic algorithms.
    '''
    def __init__(self, settings:dict):
        self.generations = settings['generations']
        self.population_size = settings['population_size']
        self.crossover_rate = settings['crossover_rate']
        self.mutation_rate = settings['mutation_rate']
        self.individual_size = settings['individual_size']

    def initialize_population(self):
        '''initilizes model with population of individuals'''
        pass

    def assess(self):
        '''scores generation based off fitness determination'''
        pass

    def repoduce(self):
        '''produces new population'''
        pass

    def simulate(self):
        '''manages genetic algorithm'''
        pass
