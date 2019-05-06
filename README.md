# fyords
A library for operations research, data science, and financial engineering.

### Info
The purpose of developing this library is for personal learning and professional
development.

**Subjects:**

1. [Open-source software development](https://en.wikipedia.org/wiki/Open-source_software_development).
2. [Data Science](https://en.wikipedia.org/wiki/Data_science).
3. [Operations Research](https://en.wikipedia.org/wiki/Operations_research).
4. [Financial Engineering](https://en.wikipedia.org/wiki/Financial_engineering).
5. [Visualizations](https://en.wikipedia.org/wiki/Data_visualization) in Python
or JavaScript.
6. Comprehensive self-education of tools such as [NumPy](https://en.wikipedia.org/wiki/NumPy),
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
The code provides everything from low level optimization engines to higher level
helper name-spaces.

### Cluster (engine)
*cluster* is aimed at identifying groups in data. See
[clustering](https://en.wikipedia.org/wiki/Cluster_analysis).

**Current Scope:**

1. [Greenfield Analysis](http://supplychaindetective.com/2017/08/12/network-strategy-part-1-greenfield-analysis/) -
a facility location and operation problem.

### Common (helper)
Grouped modules for abstracted low level functionality.

### Constraint Solver (engine)
*constraint_solver* is aimed at providing an optimization engine for
[constraint programming](https://en.wikipedia.org/wiki/Constraint_programming).

**Current Scope:**

1. [Routing](https://en.wikipedia.org/wiki/Vehicle_routing_problem) with demand,
capacity, time-windows, resource limitations and variety, pickups and
deliveries, penalties and dropping demand, ambiguous origins and destinations,
and more. More detail coming soon.
2. [Employee Scheduling](https://developers.google.com/optimization/scheduling/employee_scheduling).

### Describe (helper)
Grouped modules for descriptive statistics and general analysis of data.

### Graph Solver (engine)
This solver is limited to solutions to
[graph theory](https://en.wikipedia.org/wiki/Graph_theory) problems.

**Current Scope:**

1. [Network Flow](https://en.wikipedia.org/wiki/Flow_network) for supply chain
design.

### Learn (engine)
*learn* is aimed at leveraging [predictive](https://en.wikipedia.org/wiki/Predictive_analytics)
or [machine learning](https://en.wikipedia.org/wiki/Machine_learning)
techniques.

**Current Scope:**

1. [Neural networks](https://en.wikipedia.org/wiki/Artificial_neural_network)
for demand forecasting.
2. [Regression](https://en.wikipedia.org/wiki/Regression_analysis) for demand
forecasting.


### Linear Solver (engine)
The *linear_solver* employs solutions to [linear programming](https://en.wikipedia.org/wiki/Linear_programming)
problems.

### Normalize (helper)
Grouped modules for normalization of data. This spans [statistical](https://en.wikipedia.org/wiki/Normalization)
and [manipulative](https://en.wikipedia.org/wiki/Database_normalization)
methodologies, and the modules are not limited to preprocessing or database
management.

### Quant (TBD)
*quant* is aimed at providing [financial engineering](https://en.wikipedia.org/wiki/Financial_engineering)
modules. *quant* is not limited to specifically [financial applications of
mathematics](https://en.wikipedia.org/wiki/Mathematical_finance), but also
involves subjects pertaining to the responsibilities of a [quantitative
analyst](https://en.wikipedia.org/wiki/Quantitative_analyst). There is a lot of
overlap between OR and quantitative finance. Risk management is a good example
of this. Various modeling methodologies in quantitative finance share
similarities with both operations research and data science. For this reason
*quant* is integrated with this library.

### Simulate (engine)
*simulate* is an engine dedicated to various
*[simulation](https://en.wikipedia.org/wiki/Simulation)* suites. The word
*simulation* is used loosely here and does not limit the engine to literal
classifications of simulation.

**Current Scope:**

1. [Genetic Algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm).
2. [Stochastic Simulation](https://en.wikipedia.org/wiki/Stochastic_simulation).

### Util (helper)
Name-space for organized modules containing generally useful functions and
objects.

### Visualize (TBD)
*visualize* is aimed at providing helpful [data visualization](https://en.wikipedia.org/wiki/Data_visualization)
suites.
