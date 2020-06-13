import os

class TestConfig:
    root = os.path.dirname(os.path.abspath(__name__))
    tdir = os.path.join(root, 'tests')
    vrp_data_filepath = os.path.join(tdir, 'vrp_testing_data.csv')