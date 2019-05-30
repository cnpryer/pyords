from fyords.simulate.evaluation import SimpleFitness
from fyords.simulate.population import GeneticPopulation
from fyords.cluster.greenfield import MeanShift
from fyords.helpers.preprocess.routing import ( # example of specified package use
    haversine_distance_matrix,
    encode_random_dedicatedfleet_ga)
import pandas as pd
import numpy as np


def test_basic_usage():
    # build GA settings
    settings = {
        'generations': 20,
        'population_size': 100,
        'crossover_rate': 0.7,
        'mutation_rate': 0.2,
        'individual_size': 10, # TODO: determine appropriate number for base case
        'penalties': {} # TODO: define
    }

    # generate testing lat and lon data
    n = 100
    data = pd.DataFrame({
        'origin_lat': np.random.uniform(low=-100.0, high=100.0, size=(n,)),
        'origin_lon': np.random.uniform(low=-100.0, high=100.0, size=(n,)),
        'dest_lat': np.random.uniform(low=-100.0, high=100.0, size=(n,)),
        'dest_lon': np.random.uniform(low=-100.0, high=100.0, size=(n,)),
        'demand': np.random.randint(low=1, high=10, size=(n,))
        # TODO: windows and other constraints
    })

    # build locations list starting with origin (TODO: preprocessing multi-
    # origin routing models)
    locations = list([data[['origin_lat', 'origin_lon']].iloc[0].tolist()])

    # aggregate demand
    data = data.groupby(['origin_lat', 'origin_lon', 'dest_lat', 'dest_lon'])\
        .sum().reset_index()

    # append destinations with demand to locations
    locations += list(zip(data.dest_lat.tolist(), data.dest_lon.tolist()))
    locations = np.array([np.array(loc) for loc in locations]) # convert tuples

    # build demands
    demands = np.array([0] + data.demand.tolist())

    # build distance matrix
    lats = np.array([loc[0] for loc in locations])
    lons = np.array([loc[1] for loc in locations])
    distances = np.array(haversine_distance_matrix(lats, lons, 'mi'))

    # TODO: build time windows
    windows = np.array([np.nan for loc in locations])

    # build vehicles
    vehicles = np.array([45 for i in range(0, 2)])

    # TODO: build routes mapping using clustering
    # for now initialize with rndom list of route sets
    routes = encode_random_dedicatedfleet_ga(
        distances,
        settings['population_size']
        )

    # TODO: build routes mapping using clustering
    # for now initialize with rndom list of route sets
    population = encode_random_dedicatedfleet_ga(
        distances,
        settings['population_size']
        )

    # Fitness should be relative to the problem to be
    # solved.
    def fitness(individual, constants):

        # distance evaluation
        def get_distance(x,y):
            return constants['distances'][x][y]

        distance_scores = []
        if individual is None:
            return np.inf
        for element in individual:
            tmp = []
            for i in range(len(element)-1):
                x, y = element[i], element[i+1]
                tmp.append(get_distance(x,y))
            distance_scores.append(sum(tmp))
        return sum(distance_scores)

    # Initializing the GeneticP opulation without passing
    # any configuration will set up default components.
    constants = {
        'distances': distances}
    fitness_assessment = SimpleFitness(function=fitness, constants=constants)
    simulation = GeneticPopulation(
        population=population,
        fitness=fitness_assessment)

    simulation.run()
    assert simulation.population.shape == population.shape