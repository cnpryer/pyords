class BasicEnvironment:
    """Object to pass containing data used for solve. Individuals are mapped
    to this data upon evaluation. Environments also hold additional evaluation
    data."""
    def __init__(self, df, _dict=None):
        self.df = df
        self._dict = _dict
