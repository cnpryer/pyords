"""
routing.py - Basic models will contain single-depot multiple-truck fleets and
require adherence to a plethora of regulations.

TODO:
    -Eventually improve upon single-depot limitations.
"""
import numpy as np

class DedicatedFleet:
    """DedicatedFleet optimizes operations requiring routes for a
    dedicated fleet transporting goods. Dedicated fleets inherently must
    return to their origins.
    """
    def __init__(self, distances: list, windows: list, demands: list,
                 vehicles: list):
        """
        Parameters
        ----------
        distances: matrix of all-to-all distances (defines order).
        times: array of time windows for each location (follows order).
        demands: array of demands for each location.
        vehicles: array of capacities representing a vehicle.
        """
        self.distances = distances
        self.windows = windows
        self.demands = demands
        self.vehicles = vehicles

class AmbiguousFleet:
    """AmbiguousFleet optimizes operations requiring routes for the
    transportation of goods, irrespective of a identifiable fleet. This
    will typically involve brokered trucks.
    """
    def __init__(self):
        pass
