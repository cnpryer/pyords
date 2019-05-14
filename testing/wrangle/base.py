from fyords.util.wrangle import PandasWrangler
import numpy as np
import pandas as pd

def test_wrapper_initialization(df):
    manager = PandasWrangler(df)
    print('TESTING WRAPPER INITIALIZATION')
    print(manager.df.shape)
    print(manager.get_df())

def test_wrapper_checks(df):
    manager = PandasWrangler(df)
    print('TESTING CHECKS')
    print('nulls:', manager.check_nulls())
    print('zeros:', manager.check_zeros())
    print('negatives:', manager.check_negatives())


if __name__ == '__main__':
    df = pd.DataFrame(
        np.random.randint(0,100,size=(100, 4)),
        columns=list('ABCD'))

    test_wrapper_initialization(df)
    #test_wrapper_checks(df)
