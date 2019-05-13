# constraint_solver
*constraint_solver* is aimed at providing an optimization engine for
[constraint programming](https://en.wikipedia.org/wiki/Constraint_programming).

## Modules
1. *routing.py* - route geographical and directional demand for a singular
origin node. This is typically used in designing and optimizing supply chains.
For the sake of startup complexity, the module will start with constraints such
as demand, capacity, time-windows, resource limitations and variety, pickups and
deliveries, penalties and dropping demand, and ambiguous origins and
destinations.

## Plan
This name-space should work more as an engine with various algorithms to perform
different optimizing techniques. Helper code will be abstracted to another
name-space.
