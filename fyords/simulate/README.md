# simulate
*simulate* is an engine dedicated to various
*[simulation](https://en.wikipedia.org/wiki/Simulation)* suites. The word
*simulation* is used loosely here and does not limit the engine to literal
classifications of simulation.

## Modules
1. *crossdock.py* - simulate cross-docking.
2. *schedule.py* - leverage simulated evolution of schedules through a genetic
algorithm.
3. *routing.py* - leverage *simulation* algorithms to tackle VRP.
4. *base.py* - module housing various *simulation* algorithm/engine code.

### TODO:
5. *evaluation/* - name-space for evaluation modules. Fitness evaluations,
performance grading, etc. are defined here.
6. *initialization/* - name-space for initialization modules. Initialize random
states, intentional states, etc. using defined classes and functions here.
7. *operation/* - name-space for operator modules. Operations applied to data
within a *simulation* are defined here such as GA mutation, crossover, etc.
8. *population/* - name-space for population modules. Individual and population
objects for *simulations* are defined here.
9. *util/* - name-space for *simulation* helper functions and objects.

## Plan
This module should work more as an engine with various algorithms to perform
different simulation techniques. Helper code will be abstracted to another
name-space. Ideal genetic algorithm design will be modeled after
[evolute](https://github.com/csxeba/evolute). The architecture of evolute will
be a shared architecture for other *simulate* functionality beyond genetic
algorithms.
