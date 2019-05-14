# population
*population* is a name-space for population modules. Individual and population
objects for *simulations* are defined here.

## Modules
1. *base* - *population* name-space wrapper module.
2. *individual* - module defining elements of populations and their specific
composition profile.

## Plan
Ideally the elements of this name-space will be exposed within its instance
to allow for *population*-level access. Individuals can make up a population, so
the grading of an individuals fitness can be tied to the Individual class. The
use and setup of a GA using this name-space is still under development (TBD).
