"""Use case for solving VRP using a genetic algorithm"""
from ..pyords.genetic_algorithm import BasicGeneticAlgorithm
from ..pyords.genetic_algorithm import environments as envs
from ..pyords.genetic_algorithm.visualizations import BasicAlgoHelper
import matplotlib.pylab as lab
import pandas as pd
import numpy as np
from os import path
from haversine import haversine, Unit
import random
import logging

root_dir = path.dirname(path.abspath(__name__))
this_dir = path.join(root_dir, 'tests')

n_generations = 10
population_size = 10

# each index position of the first individual maps to same position in
# its environment data (in this case demand_data).
demand_data = pd.read_csv(path.join(this_dir, 'vrp_testing_data.csv'))
n = len(demand_data)
initial_route_ids = np.random.randint(0, n-1, n) # random first individual

# set up individuals' environment with dataframe for the solve and
# {'zip_lookup': df, 'distance_matrix': []} to use within fitness_func.
# create a lookup for unique zip code positions in distance_matrix
geo_lookup = demand_data[['zipcode', 'latitude', 'longitude']]\
    .drop_duplicates()
geo_lookup['position'] = list(range(len(geo_lookup)))
zip_lookup = geo_lookup.reset_index()[['zipcode', 'position']]

# add distance_matrix-relative position to demand data zipcodes
position_dict = dict(zip(geo_lookup.zipcode, geo_lookup.position))
demand_data['zip_i'] = demand_data.zipcode.replace(position_dict)

# create corresponding distance matrix
distance_matrix = []
indicies = geo_lookup.index.tolist()
for i in indicies:
    o_lat = geo_lookup.latitude.loc[i]
    o_lon = geo_lookup.longitude.loc[i]
    tmp_dist_li = []
    for j in indicies:
        d_lat = geo_lookup.latitude.loc[j]
        d_lon = geo_lookup.longitude.loc[j]
        dist = haversine((o_lat, o_lon), (d_lat, d_lon), Unit.MILES)
        tmp_dist_li.append(dist*1.17) # assumed circuity
    distance_matrix.append(tmp_dist_li)
environment_dict = {'distance_matrix': distance_matrix}

def fitness_func(individual, environment):
    """Return a fitness score for an individual. Lower scores rank
    higher."""

    def decode():
        """return individual represented with demand_data"""
        data = environment.df.copy()
        data['chromosomes'] = individual
        return data

    decoded = decode()

    # evaluate routes' total weight, total pallets, and total distance.
    max_weight = 45000
    max_pallets = 25
    max_distance = 50*2 # represent a total day of driving based off of 2 stops

    # tally penalties (dif from maxing out capacity + minimizing distance)
    weight_penalty = (
        max_weight - decoded.groupby('chromosomes')['weight'].sum()
        ).abs().sum()

    pallet_penalty = (
        max_pallets - decoded.groupby('chromosomes')['pallets'].sum()
        ).abs().sum()

    def get_distance(c1, c2, i1, i2):
        if i1 < 0:
            return np.nan
        if c1 != c2:
            return np.nan
        return environment._dict['distance_matrix'][int(i1)][int(i2)]

    def get_distance_penalty():
        decoded.sort_values(by='chromosomes', inplace=True)
        decoded['prev_i'] = decoded.zip_i.shift().fillna(-1).astype(int)
        decoded['prev_chromosomes'] = decoded.chromosomes.shift()
        decoded['distance'] = decoded.apply(lambda x: get_distance(
            x.prev_chromosomes, x.chromosomes, x.prev_i, x.zip_i), axis=1)
        return decoded.distance.sum()

    distance_penalty = get_distance_penalty()
    total_penalty = weight_penalty + pallet_penalty + distance_penalty
    return total_penalty

def test_algorithm():
    # visualization for fitness algo performance
    lab.close('all')
    viz = BasicAlgoHelper()

    # configure algorithm
    environment = envs.BasicEnvironment(df=demand_data, _dict=environment_dict)
    algorithm = BasicGeneticAlgorithm(
        first_individual=initial_route_ids,
        environment=environment,
        fitness_func=fitness_func,
        n_generations=n_generations,
        population_size=population_size,
        mutation_rate=0.07,
        viz=viz)
    result = algorithm.run()
    assert len(result) == len(demand_data)

if __name__ == '__main__':
    test_algorithm()
