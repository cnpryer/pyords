import numpy as np
import pandas as pd

class ModificationsBase:
    def __init__(self):
        pass

class SimpleDrops(ModificationsBase):
    def __init__(self):
        ModificationsBase.__init__(self)

class SimpleFills(ModificationsBase):
    def __init__(self):
        ModificationsBase.__init__(self)

Drops = SimpleDrops
Fills = SimpleFills
