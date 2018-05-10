import pandas as pd
import colors


def ex(items, each=lambda x: {}, constant={}):
    rows = []
    for item in items:
        dct = each(item)
        dct.update(constant)
        rows.append(dct)
    return rows


def comb(rows):
    # TODO: Add some asserts.
    return pd.DataFrame(rows)


class Series(object):
    """
    Wraps Pandas series (index, data points)
    and error bars (optional)
    and metadata (colour, title for plotting line)
    """
    def __init__(self,
                 series=None,
                 y=None,
                 x=None,
                 name=None,
                 plotstyle=None,
                 **kwargs):
        assert series is None or (x is not None and y is not None)
        if series is None:
            self.series = pd.Series(data=y, index=x, name=name, **kwargs)
        else:
            self.series = series
            if name is not None:
                self.series.name = name
        if isinstance(plotstyle, str):
            plotstyle = colors.SERIES[plotstyle]
        self.plotstyle = plotstyle
