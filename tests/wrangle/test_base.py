from fyords.helpers.wrangle import PandasWrangler
import numpy as np
import pandas as pd

def get_basic_data():
    return pd.DataFrame(
        np.random.randint(0,100,size=(100, 4)),
        columns=list('ABCD'))

def test_random_data_initialization():
    assert isinstance(get_basic_data(), (pd.DataFrame,))

def test_wrapper_initialization():
    df = get_basic_data()
    manager = PandasWrangler(df)
    assert isinstance(manager.df, (pd.DataFrame))

