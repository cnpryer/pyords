from .selection import SimpleSelection
from .crossover import SimpleCrossover
from .mutate import SimpleMutation
from .base import Operation

__docs__ = ''
with open('./README.md') as f:
    __docs__ = f.read()
