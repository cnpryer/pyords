import numpy as np
import pandas as pd

class PandasWrapper:
    '''
    Purpose:
        Provide agnostic data wrangling object as a helper for working with
        data. Current scope of this class handles data work pertaining to a
        modeling process based in pandas.
    '''
    def __init__(self, df:pd.DataFrame):
        self.set_df(df)

    def set_df(self, df:pd.DataFrame):
        '''
        Purpose:
            Set instance data to wrap with PandasWrangler.

        Args:
            df: pandas dataframe used in wrangling process of an analysis.
        '''
        self.df = df.copy()

    def get_df(self):
        '''
        Purpose:
            Return the PandasWrangler instance data.
        '''
        return self.df

    def zeros(self, method:str='describe'):
        '''
        Purpose:
            Identify data with values of zeros for review, alteration, or
            exclusion.

        Args:
            method: options of 'describe', 'modify', 'exclude'.
            -'describe' prints statistics about the representation of zeros
            in self.df and the potential impact of dropping it.
            -modify TBD
            -exclude drops data with values of zero and prints impact.
        '''
        pass

    def nulls(self, method:str='describe'):
        '''Currently not utilized in helper modules (df.isnull().sum())'''
        pass

    def negative(self, method:str='describe'):
        '''
        Purpose:
            Identify data with values of null for review, alteration, or
            exclusion.

        Args:
            method: options of 'describe', 'modify', 'exclude'.
            -'describe' prints statistics about the representation of zeros
            in self.df and the potential impact of dropping it.
            -modify TBD
            -exclude drops data with values of zero and prints impact.
        '''
        pass
