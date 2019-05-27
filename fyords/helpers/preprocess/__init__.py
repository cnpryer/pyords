from .distance import haversine, haversine_vectorized
from .routing import (
    haversine_distance_matrix,
    encode_random_dedicatedfleet_ga,
    encode_clustered_dedicatedfleet_ga)
from .scgx import LlamaLoader, LlamaStage

__docs__ = ''
with open('./README.md') as f:
    __docs__ = f.read()
