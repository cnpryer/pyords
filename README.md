(In Development)

![python package](https://github.com/christopherpryer/pyords/workflows/Python%20package/badge.svg)

# pyords
A library for operations research and data science.

## implementation types

- graph theory
- genetic algorithm
- simulation
- machine learning

## motivation behind the project
Self-learning:

1. [Open-source software development](https://en.wikipedia.org/wiki/Open-source_software_development)
2. [Data Science](https://en.wikipedia.org/wiki/Data_science)
3. [Operations Research](https://en.wikipedia.org/wiki/Operations_research)
4. [Financial Engineering](https://en.wikipedia.org/wiki/Financial_engineering)
5. [Visualizations](https://en.wikipedia.org/wiki/Data_visualization) in Python
or JavaScript
6. Big splash! [NumPy](https://en.wikipedia.org/wiki/NumPy),
[Pandas](https://en.wikipedia.org/wiki/Pandas_(software)),
[D3.js](https://en.wikipedia.org/wiki/D3.js),
[Plotly](https://plotly.com/),
[Matplotlib](https://en.wikipedia.org/wiki/Matplotlib),
[IPython](https://en.wikipedia.org/wiki/IPython) and [jupyter](https://en.wikipedia.org/wiki/Project_Jupyter),
[scikit-learn](https://en.wikipedia.org/wiki/Scikit-learn) and [SciPy](https://en.wikipedia.org/wiki/SciPy),
[git](https://en.wikipedia.org/wiki/Git),
[Google OR Tools (ortools)](https://developers.google.com/optimization/),
[Pyomo](https://en.wikipedia.org/wiki/Pyomo),
[Supply Chain Guru](https://www.llamasoft.com/products/design/supply-chain-guru/),
[Keras](https://en.wikipedia.org/wiki/Keras), [Hadoop](https://en.wikipedia.org/wiki/Apache_Hadoop),
[AWS](https://en.wikipedia.org/wiki/Amazon_Web_Services),
[GCP](https://en.wikipedia.org/wiki/Google_Cloud_Platform), [Vagrant](https://www.vagrantup.com/)

# Development & Documentation
## pyords ```Bundle```s

```Bundle```s are self-contained problem definitions implemented as modular instances. That's wanna-be fancy for packaged units of code that are very plug-in and play. Contributing to ```Bundle``` development:

1. Design the problem as a ```Case``` where the ```Case``` can be tested against various ```Bundle```s that solve the problem defined in the ```Case```. For the purposes of this ```README``` we'll use ```VrpVehicleCase```. ```Case```s must help define what is required of a feature implementation (or the improvement of one). For our ```VrpVehicleCase``` we'll assume a set of data and configurations for basic vrp model requirements and a desired output of optimized vehicles to append to our data.

2. Build a ```Bundle```. The bundle should be specific to the ```Case```(s) it solves. Maybe you see where I'm going with this. There are **two** core components of this library:
    - ```Bundle```s
    - ```Case```s

3. Test the ``Case`` against its ```Bundle```. 

4. Submit implementation with documentation supporting the reason for its development.

### ```VrpVehicleCase```
- defines allowable data for one or many vehicles outputs via vrp optimization
- defines input expectations & tests
- defines ```Case``` expectations & tests
- defines output expectations & tests
- related:
  - GeoBundle
  - OrBundle

### ```GeoBundle```
- processed zipcode outputs, lat and lon outputs, haversine distance outputs, and lat and lon cluster outputs
- integrations:
  - lats lons: [pgeocode](https://github.com/symerio/pgeocode)
  - distances: [haversine](https://github.com/mapado/haversine)
- related:
  - ZipcodeCleanCase
  - LatLonCase
  - LatLonDistanceCase
  - LatLonClusterCase

### ```OrBundle```
- operations research optimizations: vrp, network optimization, scheduling.
- opportunity analysis, health checks.
- implementations:
  - Vrp optimization via Google OrTools
  - Schedule optimization via Genetic Algorithm
- integrations: 
  - vrp: [google ortools](https://github.com/google/or-tools)

## using pyords ```Bundle```s for vehicle optimization

```python
import pyords as pyr


df = pd.read_csv('my_shipment_data.csv')

geobndl = pyr.GeoBundle(zipcodes=df.zipcodes)
lats, lons = geo_bndl.pgeo('US')
matrix = geobndl.haversine_all_from(origin=origin, 'mi')
clusters = geobndl.cluster(by='geocodes')

orbndl = pyr.OrBundle(matrix=matrix, demand=df.pallets)

vehicles = orbndl.ortools.vrp( 
    depot_index=0, # required
    max_vehicle_capacity=26, # default: 26
    max_search_seconds=30, # default 30
    partitions=clusters, # optional TODO: allow for distributed
    return_solution=True # optional
)

live_vehicles_returned = [v for v in vehicles if len(v['stops'][1:-1]) > 0]

assert orbndl.vehicles.pull('n.utilized') == len(live_vehicles_returned)

df['vehicles'] = orbndl.pull('vehicle_id')
```

## Testing pyords ```Bundle```s :white_check_mark:

```python
import pyords as pyr

class VrpVehicleCase:
    inputs = {
        'matrix': [[0, 1, 2], [1, 0, 2], [2, 2, 0]],
        'demand': [0, 3, 4],
        'max_vehicle_capacity': 5,
        'partitions': [1, 1, 1]
    }

    outputs = {
        'vehicle_id': [1, 2]
    }

    implementation = pyr.OrBundle.ortools.vrp

    def run():
        bndl = pyr.OrBundle(case=VrpVehicleCase)

        assert bndl.test()

if __name__ == '__main__':
    VrpVehicleCase.run()
```
