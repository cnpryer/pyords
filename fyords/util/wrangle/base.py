'''TODO: make this a pandas extension'''
from . import SimpleCompostitionChecks, Fills, Drops
import numpy as np
import pandas as pd

class PandasWrangler:
    def __init__(self, df:pd.DataFrame):
        self.set_df(df)

    def set_df(self, df:pd.DataFrame):
        self.df = df.copy()

    def get_df(self):
        return self.df
