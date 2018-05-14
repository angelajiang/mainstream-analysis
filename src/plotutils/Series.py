import numpy as np
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
    # TODO: Add some asserts, e.g. to check consistency between rows
    return pd.DataFrame(rows)


def agg2xy(aggregated, names=None):
    unstacked = aggregated.unstack(0)
    if names is None:
        names = unstacked.columns
    xss, yss = zip(*[(unstacked[k].index, unstacked[k].values) for k in names])
    return xss, yss


def agg2series(aggregated, names=None, **kwargs):
    xss, yss = agg2xy(aggregated, names=names)
    return get_series(xss, yss, names=names, **kwargs)


def get_series(xss, yss, errs=None, names=None, plotstyles=None, plotparams={}):
    if plotstyles is None:
        plotstyles = names
    elif isinstance(plotstyles, dict):
        plotstyles = [plotstyles[k] for k in names]
    if errs is not None:
        return [Series(x=xs, y=ys, yerrs=yerr, name=sn, plotstyle=ps, plotparams=plotparams)
                for xs, ys, yerr, ps, sn in zip(xss, yss, errs, plotstyles, names)]
    return [Series(x=xs, y=ys, name=sn, plotstyle=ps, plotparams=plotparams)
            for xs, ys, ps, sn in zip(xss, yss, plotstyles, names)]


def get_errors(y, e_delta=None, e_abs=None):
    assert e_delta is None or e_abs is None, "Supply EITHER e_delta or e_abs"
    # matplotlib expects either an array of [deltas], or [-delta, +delta]
    if e_delta is not None:
        return e_delta
    else:
        assert len(e_abs) == 2
        assert len(e_abs[0]) == len(y) and len(e_abs[1]) == len(y)
        e_abs = map(np.asarray, e_abs)
        y = np.asarray(y)
        return [y - e_abs[0], e_abs[1] - y]


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

    def x(self):
        return self.series.index

    def y(self):
        return self.series.values

    def __repr__(self):
        return str(self.series)