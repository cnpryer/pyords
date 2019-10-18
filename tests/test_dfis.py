"""Demand Forecastability for Inventory Strategy"""
import pandas as pd
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__name__))
TEST_DATA_FILENAME = 'dfis_testing_data.csv'
TEST_CONFIG_FILENAME = 'dfis_testing_config.csv'

def process_datetime(series):
    return pd.to_datetime(
        series, infer_datetime_format=True, errors='coerce')

df = pd.read_csv(os.path.join(ROOT_DIR, 'tests', TEST_DATA_FILENAME))
df.request_date = process_datetime(df.request_date) # TODO: agnostic dates

config = pd.read_csv(os.path.join(ROOT_DIR, 'tests', TEST_CONFIG_FILENAME))

def get_attributes(level):
    return config[config.level==level].attributes.str.split('+').tolist()[0]

def get_period(period_len='Q', date_col='request_date', num_col='quantity'):
    _cols = [col for col in df.columns if col not in [date_col, num_col]]
    return df.groupby(_cols + [pd.Grouper(key=date_col, freq=period_len)])\
        [num_col].sum().reset_index()

def get_adi(period_df, attributes, num_col='quantity'):
    """
    𝐴𝐷𝐼=𝑝𝑛/𝑑𝑛

    𝑝𝑛 : number of periods
    𝑑𝑛 : number of demands
    𝐴𝐷𝐼 : Average Demand Interval
    """
    aggfunc = {num_col: ['sum', 'count']}
    result = period_df.groupby(attributes).agg(aggfunc)
    return result[(num_col, 'count')] / result[(num_col, 'sum')]

def get_cv2(attributes, num_col='quantity'):
    """
    𝐶𝑉2=(𝜎𝑝/𝜇𝑝)2

    𝜎𝑝: standard deviation of population
    𝜇𝑝: average of population
    𝐶𝑉2: coefficient of variation
    """
    aggfunc = {num_col: ['std', 'mean', 'count']}
    result = df.groupby(attributes).agg(aggfunc)
    return (result[(num_col, 'std')] / result[(num_col, 'mean')]) ** 2

def calculate_smooth(period_df, attributes=['sku', 'origin_id'],
    num_col='quantity'):
    adi = get_adi(period_df, attributes, num_col)
    cv2 = get_cv2(attributes, num_col)
    is_smooth = (adi < 1.32) & (cv2 < 0.49)
    return is_smooth.sum() / len(is_smooth)

def test_main():
    period_df = get_period(period_len='Q')
    assert not period_df.empty

    attributes = config.attributes.str.split('+').tolist()[0]
    result = calculate_smooth(period_df, attributes)
    assert result <= 1 and result >= -1

if __name__ == '__main__':
    test_main()
