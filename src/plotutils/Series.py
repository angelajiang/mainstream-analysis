import pandas as pd


class Series(object):
    """
    Wraps Pandas series (index, data points)
    and error bars (optional)
    and metadata (colour, title for plotting line)
    """
    def __init__(self,
                 data=None,
                 index=None,
                 name=None,
                 colour
                 **kwargs):
        self.series = pd.Series(data=data, index=index, name=name, **kwargs)
