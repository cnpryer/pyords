"""
Basic models will contain single-depot multiple-truck fleets and require
adherence to a plethora of regulations.

TODO:
    -Eventually improve upon single-depot limitations.
"""
import numpy as np

class DedicatedFleet:
    """
    Purpose:
        DedicatedFleet optimizes operations requiring routes for a
        dedicated fleet transporting goods. Dedicated fleets inherently must
        return to their origins.
    """
    def __init__(self, distances:np.array, windows:np.array, demands:np.array,
    vehicles:np.array):
        """
        Args:
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
    """
    Purpose:
        AmbiguousFleet optimizes operations requiring routes for the
        transporation of goods, irrespective of a indentifiable fleet. This
        will typically involve brokered trucks.
    """
    def __init__(self):
        pass
