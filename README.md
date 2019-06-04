[![CircleCI](https://circleci.com/gh/christopherpryer/fyords/tree/master.svg?style=svg)](https://circleci.com/gh/christopherpryer/fyords/tree/master)
[![codebeat badge](https://codebeat.co/badges/f72db301-fd66-4c05-b1ca-9b8c8196f06e)](https://codebeat.co/projects/github-com-christopherpryer-fyords-master)

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

### Base (TBD)
Grouped modules for abstracted *fyords* functionality.

### Constraint Solver (engine)
*constraint_solver* is aimed at providing an optimization engine for
[constraint programming](https://en.wikipedia.org/wiki/Constraint_programming).

**Current Scope:**

1. [Routing](https://en.wikipedia.org/wiki/Vehicle_routing_problem) with demand,
capacity, time-windows, resource limitations and variety, pickups and
deliveries, penalties and dropping demand, ambiguous origins and destinations,
and more. More detail coming soon.
2. [Employee Scheduling](https://developers.google.com/optimization/scheduling/employee_scheduling).

### helpers/Describe (helper)
Grouped modules for descriptive statistics and general analysis of data.

**Current Scope:**

1. Logistics-based opportunities

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

### helpers/Preprocess (helper)
Name-space for preprocessing data.

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

### helpers
Name-space for organized modules containing generally useful functions and
objects.

**Current Scope:**

1. Pandas-dataframe-based wrangling


### helpers/Visualize (TBD)
*visualize* is aimed at providing helpful [data visualization](https://en.wikipedia.org/wiki/Data_visualization)
suites.

### helpers/Wrangle
Name-space for data wrangling wrappers and helpers.

## Collaborating
Since this is a learning project, the code will be developed with the
intention of solving a real-world problem pertaining to the developer. This
will impact the evolution of this library's design. An example of this taylored
design would be the module in the *constraint_solver* name-space. This
name-space is intended to house a constraint programming engine with
problem-agnostic design. Early on a *routing.py* module will house specified
modeling such as *DedicatedFleet* and *AmbiguousFleet*. It is required for this
evolution of design strategy to be followed if you would like to collaborate.
Each problem-set must be developed in its own feature branch.
