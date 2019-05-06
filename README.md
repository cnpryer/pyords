# pryords
A library for operations research and data science.

## Domain
The intended use of this code is for logistics-oriented problems but is not
limited to logistics.

## Info
The purpose of developing this library is for personal learning and professional
development purposes.

### Subjects:
1. [Open-source software development](https://en.wikipedia.org/wiki/Open-source_software_development).
2. [Data Science](https://en.wikipedia.org/wiki/Data_science) in Python.
3. [Operations Research](https://en.wikipedia.org/wiki/Operations_research).
4. [Visualizations](https://en.wikipedia.org/wiki/Data_visualization) in Python
or JavaScript.
5. Comprehensive self-education of tools such as [NumPy](https://en.wikipedia.org/wiki/NumPy),
[Pandas](https://en.wikipedia.org/wiki/Pandas_(software)),
[D3.js](https://en.wikipedia.org/wiki/D3.js),
[Matplotlib](https://en.wikipedia.org/wiki/Matplotlib),
[IPython](https://en.wikipedia.org/wiki/IPython) and [jupyter](https://en.wikipedia.org/wiki/Project_Jupyter),
[scikit-learn](https://en.wikipedia.org/wiki/Scikit-learn) and [SciPy](https://en.wikipedia.org/wiki/SciPy),
[git](https://en.wikipedia.org/wiki/Git),
[Google OR Tools (ortools)](https://developers.google.com/optimization/),
[Pyomo](https://en.wikipedia.org/wiki/Pyomo),
[Supply Chain Guru](https://www.llamasoft.com/products/design/supply-chain-guru/),
[Keras](https://en.wikipedia.org/wiki/Keras) and/or [Hadoop](https://en.wikipedia.org/wiki/Apache_Hadoop),
[AWS](https://en.wikipedia.org/wiki/Amazon_Web_Services),
[GCP](https://en.wikipedia.org/wiki/Google_Cloud_Platform).


## The Library
The code is broken down into relevant name-spaces to handle various logistics
problems.

### Cluster
*cluster* is aimed at identifying groups in data. See
[clustering](https://en.wikipedia.org/wiki/Cluster_analysis).

**Current Scope:**

1. [Greenfield Analysis](http://supplychaindetective.com/2017/08/12/network-strategy-part-1-greenfield-analysis/) -
a facility location and operation problem.

### Common
Grouped modules for abstracted low level functionality.

### Constraint Solver
*constraint_solver* is aimed at providing an optimization engine for
[constraint programming](https://en.wikipedia.org/wiki/Constraint_programming).

**Current Scope:**

1. [Routing](https://en.wikipedia.org/wiki/Vehicle_routing_problem) with demand,
capacity, time-windows, resource limitations and variety, pickups and
deliveries, penalties and dropping demand, ambiguous origins and destinations,
and more. More detail coming soon.
2. [Network Flow](https://en.wikipedia.org/wiki/Flow_network) for supply chain
design.

### Describe
Grouped modules for descriptive statistics and general analysis of data.

### Normalize
Grouped modules for normalization of data. This spans [statistical](https://en.wikipedia.org/wiki/Normalization)
and [manipulative](https://en.wikipedia.org/wiki/Database_normalization)
methodologies, and the modules are not limited to preprocessing or database
management.

### Predict
*predict* is aimed at leveraging [predictive analytics](https://en.wikipedia.org/wiki/Predictive_analytics).

**Current Scope:**

1. [Neural networks](https://en.wikipedia.org/wiki/Artificial_neural_network)
for demand forecasting.
2. [Regression](https://en.wikipedia.org/wiki/Regression_analysis) for demand
forecasting.

### Util
Name-space for organized modules containing generally useful functions and
objects.

### Visualize
*visualize* is aimed at providing helpful [data visualization](https://en.wikipedia.org/wiki/Data_visualization)
suites.
