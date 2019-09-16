"""Use case for solving VRP using a genetic algorithm"""
from fyords.simulate.genetic_algorithm import algorithms as algs
from fyords.simulate.genetic_algorithm import environments as envs
import pandas as pd
import numpy as np
from os import path
from haversine import haversine, Unit
import random

root_dir = path.dirname(path.abspath(__name__))
instance_dir = path.join(root_dir, 'instance')

# user-defined parameters
filepath = path.join(instance_dir, 'demand.csv')
demand_data = pd.read_csv(filepath) # data to use for solve
n_generations = 10
population_size = 10

# each index position of the first individual maps to same position in
# its environment data (in this case demand_data).
n = len(demand_data)
initial_route_ids = np.random.randint(0, n-1, n) # random first individual

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
    max_distance = 50*2 # represent a total day of driving

    # tally penalties (dif from maxing out capacity + minimizing distance)
    weight_penalty = (
        max_weight - decoded.groupby('chromosomes')['Weight'].sum()
        ).abs().sum()

    pallet_penalty = (
        max_pallets - decoded.groupby('chromosomes')['Plts'].sum()
        ).abs().sum()

    def get_distance(x):
        if pd.isnull(x['1St FrZip']) or pd.isnull(x.prev_zip):
            return np.nan
        if x.chromosomes != x.prev_chromosomes:
            return np.nan
        lookup = environment._dict['zip_lookup']
        origin_condition = (lookup['1St FrZip'] == x.prev_zip)
        origin_index = lookup.loc[origin_condition, 'position'].values[0]
        dest_condition = (lookup['1St FrZip'] == x['1St FrZip'])
        dest_index = lookup.loc[dest_condition, 'position'].values[0]
        return environment._dict['distance_matrix'][origin_index][dest_index]

    def get_distance_penalty():
        decoded.sort_values(by='chromosomes', inplace=True)
        decoded['prev_zip'] = decoded['1St FrZip'].shift()
        decoded['prev_chromosomes'] = decoded.chromosomes.shift()
        decoded['distance'] = decoded.apply(get_distance, axis=1)
        return decoded.distance.sum()

    distance_penalty = get_distance_penalty()
    return weight_penalty + pallet_penalty + distance_penalty

# set up individuals' environment with dataframe for the solve and
# {'zip_lookup': df, 'distance_matrix': []} to use within fitness_func.
# create a lookup for unique zip code positions in distance_matrix
geo_lookup = demand_data[['1St FrZip', 'latitude', 'longitude']]\
    .drop_duplicates()
geo_lookup['position'] = list(range(len(geo_lookup)))

cols = ['1St FrZip', 'position']
_dict = {'zip_lookup': geo_lookup.reset_index()[cols]}

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
_dict['distance_matrix'] = distance_matrix

environment = envs.BasicEnvironment(df=demand_data, _dict=_dict)

# configure algorithm
algorithm = algs.BasicGeneticAlgorithm(
    first_individual=initial_route_ids,
    environment=environment,
    fitness_func=fitness_func,
    n_generations=n_generations,
    population_size=population_size)


def test_algorithm():
    result = algorithm.run()
    assert len(result) == len(demand_data)
    demand_data['truck_id'] = result
    demand_data.to_csv(path.join(instance_dir, 'result.csv'), index=False)

if __name__ == '__main__':
    test_algorithm()
