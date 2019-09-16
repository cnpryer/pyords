from fyords.simulate.evaluation import SimpleFitness
from fyords.simulate.population import GeneticPopulation
from fyords.cluster.greenfield import MeanShift
from fyords.helpers.preprocess.routing import ( # example of specified package use
    haversine_distance_matrix,
    encode_random_dedicatedfleet_ga)
import pandas as pd
import numpy as np


def test_basic_usage():
    # TODO: build GA settings
    # -determine appropriate number of individuals for base case
    # -define 'penalties
    settings = {
        'generations': 50,
        'population_size': 100,
        'crossover_rate': 0.7,
        'mutation_rate': 0.2,
        'individual_size': 10,
        'penalties': {}}

    # TODO: generate testing lat and lon data
    # -windows and other constraints
    n = 100
    data = pd.DataFrame({
        'origin_lat': np.array([40.5 for i in range(n)]),
        'origin_lon': np.array([-77.5 for i in range(n)]),
        'dest_lat': np.random.uniform(low=40.0, high=41.0, size=(n,)),
        'dest_lon': np.random.uniform(low=-78.0, high=-77.0, size=(n,)),
        'demand': np.random.randint(low=1, high=100, size=(n,))})

    # TODO: build locations list starting with origin
    # -improve
    locations = list([data[['origin_lat', 'origin_lon']].iloc[0].tolist()])

    # aggregate demand
    data = data.groupby(['origin_lat', 'origin_lon', 'dest_lat', 'dest_lon'])\
        .sum().reset_index()

    # append destinations with demand to locations
    locations += list(zip(data.dest_lat.tolist(), data.dest_lon.tolist()))
    locations = np.array([np.array(loc) for loc in locations]) # convert tuples

    # build demands
    demand = np.array([0] + data.demand.tolist())

    # build distance matrix
    lats = np.array([loc[0] for loc in locations])
    lons = np.array([loc[1] for loc in locations])
    distances = np.array(haversine_distance_matrix(lats, lons, 'mi'))

    # TODO: build time windows
    windows = np.array([np.nan for loc in locations])

    # build vehicles
    vehicles = np.array([45 for i in range(0, 2)])

    # TODO:
    # build routes mapping using clustering for now initialize with random list of route sets
    population = encode_random_dedicatedfleet_ga(
        distances,
        settings['population_size'])

    # Fitness should be relative to the problem to be
    # solved.
    def fitness(individual, constants):

        # distance evaluation
        def get_distance(x,y):
            return constants['distances'][x][y]

        # demand evaluation
        def get_demand(x):
            return constants['demand'][x]

        distance_total = 0
        demand_total = 0
        if individual is None:
            return np.inf
        for element in individual:
            distance = 0
            demand = 0
            for i in range(len(element)-1):
                x, y = element[i], element[i+1]
                distance += get_distance(x,y)
                demand += get_demand(x)
            distance += get_distance(element[-1], 0)
            demand += get_demand(element[-1])
            distance_total += distance
            demand_total += demand
        score = (-distance_total) + demand_total
        return score

    # Initializing the GeneticPopulation without passing
    # any configuration will set up default components.
    constants = {
        'distances': distances,
        'demand': demand}
    fitness_assessment = SimpleFitness(function=fitness, constants=constants)
    simulation = GeneticPopulation(
        population=population,
        fitness=fitness_assessment,
        generations=settings['generations'])

    simulation.run()
    assert len(simulation.population) == len(population)
