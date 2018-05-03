import pandas as pd


class Series(object):
    """
    Wraps Pandas series (index, data points)
    and error bars (optional)
    and metadata (colour, title for plotting line)
    """
    def __init__(self):
        self.series = pd.Series()
