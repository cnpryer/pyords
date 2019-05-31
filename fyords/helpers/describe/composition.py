import numpy as np
import pandas as pd

class CompositionBase:
    def __init__(self):
        pass

    def describe(self, conditions: tuple, df: pd.DataFrame, label: str='Info'):
        index = df.loc[conditions].index.tolist()
        x = len(df)
        y = len(index)
        d = x-y
        msg = ('{}:\n'
                'df rows: {}\n'
                'index count: {}'
                '\ndifference: {}').format(label, x, y, d)
        print(msg)

class SimpleCompostitionChecks(CompositionBase):

    def __init__(self):
        CompositionBase.__init__(self)

    def check_zeros(self, df: pd.DataFrame, columns: list):
        conditions = (df[columns].astype('float') == 0).any(axis=1)
        self.describe(conditions, df, label='Zeros')

    def check_nulls(self, df: pd.DataFrame, columns: list):
        conditions = (df[columns].isna()).any(axis=1)
        self.describe(conditions, df, label='Nulls')

    def check_negatives(self, df: pd.DataFrame, columns: list):
        conditions = (df[columns].astype('float') < 0).any(axis=1)
        self.describe(conditions, df, label='Negatives')
