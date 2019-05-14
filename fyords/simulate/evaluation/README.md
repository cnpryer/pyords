# evaluation
*evaluation* is a name-space for evaluation modules. Fitness evaluations,
performance grading, etc. are defined here.

## Modules
1. *base* - evaluation module used as a wrapper to the name-space.
2. *fitness* - currently fitness evaluation module for genetic algorithms.
3. *grading* - module defining grading types for evaluations.

## Plan
(TBD) - as of now a fitness function will be initialized with the fitness
wrapper. This fitness function will return values agnostic of impact until
further development is completed. Ideally there will be varying grading
techniques similar to evolute. The key difference with this name-space is
how the *evaluation* of an environment is an abstracted concept. So fitness
is an element. Another goal of mine is to provide a medium for self-education
of efficiency-driven solutions in python. So I'd like to see how the footprint
of classes impacts run-time.
