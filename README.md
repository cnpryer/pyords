![](https://github.com/christopherpryer/pyords/workflows/build/badge.svg)

# pyords
A library for operations research, data science, and financial engineering.

## features

- pyords.transopt - transportation optimization
- pyords.netopt - network optimization
- pyords.schedopt - schedule optimization

## implementations

- graph theory
- genetic algorithm
- simulation
- machine learning

## motivation behind the project
Working solo in an engineering team, I want to dedicate a fair amount of time to productionalizing the different skills I've been working on. This library will help me expose myself more to the following:

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
[GCP](https://en.wikipedia.org/wiki/Google_Cloud_Platform), [Vagrant](https://www.vagrantup.com/).

# Development & Documentation
Design is up for discussion. I'm going to start by just *namespacing* most of the unique features implemented. Some currently developed features include the following:

### cluster
*cluster* is aimed at identifying groups in data. See
[clustering](https://en.wikipedia.org/wiki/Cluster_analysis).

#### current scope

1. [Greenfield Analysis](http://supplychaindetective.com/2017/08/12/network-strategy-part-1-greenfield-analysis/) -
a facility location and operation problem. *cluster* will provide a clustering
algorithm for heuristic solutions.

2. Route heuristic for clustering final-destination demand nodes by proximity.

### genetic_algorithm
[Genetic Algorithm](https://en.wikipedia.org/wiki/Genetic_algorithm).

### solver
1. [Route optimization](https://en.wikipedia.org/wiki/Vehicle_routing_problem).

### distance
1. [Haversine distance](https://en.wikipedia.org/wiki/Haversine_formula).
2. Distance matrix preprocessing.