import pandas as pd
import styles


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


def agg2xy(aggregated, names=None):
    unstacked = aggregated.unstack(0)
    if names is None:
        names = unstacked.columns
    xss, yss = zip(*[(unstacked[k].index, unstacked[k].values) for k in names])
    return xss, yss


def get_series(xss, yss, series_names=None, plotstyles=None, plotparams={}):
    if plotstyles is None:
        plotstyles = series_names
    return [Series(x=xs, y=ys, name=sn, plotstyle=ps, plotparams=plotparams)
            for xs, ys, ps, sn in zip(xss, yss, plotstyles, series_names)]


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
                 yerrs=None,
                 name=None,
                 plotstyle=None,
                 plotparams=None,
                 **kwargs):
        assert series is None or (x is not None and y is not None)
        if series is None:
            self.series = pd.Series(data=y, index=x, name=name, **kwargs)
        else:
            self.series = series
            if name is not None:
                self.series.name = name
        if yerrs is not None:
            assert len(yerrs) == len(self.series)
            if len(yerrs) > 0:
                assert len(yerrs[0]) in (1, 2)
        if isinstance(plotstyle, str):
            plotstyle = styles.SERIES[plotstyle]
        self.plotstyle = plotstyle
        self.yerrs = yerrs
        self.plotparams = plotparams

    def plot(self, *args, **kwargs):
        if self.plotparams is not None:
            kwargs.update(self.plotparams)
        if self.yerrs is not None:
            kwargs['yerr'] = self.yerrs
        for k in ['marker', 'color', 'label']:
            kwargs[k] = self.plotstyle[k]
        self.series.plot(*args, **kwargs)

    def __repr__(self):
        return str(self.series)