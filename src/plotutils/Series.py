import warnings
import numpy as np
import pandas as pd
import styles


def ex(items, each=lambda s: s.to_map(), constant={}):
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
    for k in names:
        if k not in unstacked.columns:
            warnings.warn("Missing series " + k)
    names = [k for k in names if k in unstacked.columns]
    xss, yss = zip(*[(unstacked[k].index, unstacked[k].values) for k in names])
    return xss, yss


def agg2series(aggregated, names=None, errs=None, **kwargs):
    xss, yss = agg2xy(aggregated, names=names)
    if errs is not None:
        # TODO: Split up the errors
        # In: dict(e_delta=[low, high])
        # Out: [dict(e_delta=[low, high]), ...]
        assert isinstance(errs, dict) and len(errs) == 1
        err_type, errs_v = errs.items()[0]
        try:
            len(errs_v[0])
        except TypeError:
            errs_v = [errs_v]
        new_errs = []
        for errA in errs_v:
            xss_e, yss_e = agg2xy(errA, names=names)
            assert len(xss) == len(xss_e) == len(yss_e)
            for xs, xe in zip(xss, xss_e):
                assert tuple(xs) == tuple(xe), "Order of indexes for data and errors do not match"
            new_errs.append(yss_e)
        if len(new_errs) == 1:
            errs = [{err_type: err_} for err_ in new_errs[0]]
        else:
            errs = [{err_type: err_} for err_ in zip(*new_errs)]
    return get_series(xss, yss, names=names, errs=errs, **kwargs)


def get_series(xss, yss, errs=None, names=None, plotstyles='names', plotparams={}):
    """Pass plotstyles=None for throwaway plots"""
    if plotstyles is None:
        plotstyles = [None for _ in range(len(xss))]
    elif plotstyles == 'names':
        plotstyles = names
    elif isinstance(plotstyles, dict):
        plotstyles = [plotstyles[k] for k in names]
    if not isinstance(plotparams, dict) and isinstance(plotparams, str):
        plotparams = styles.LINEGROUPS[plotparams]
    if errs is not None:
        assert len(xss) <= len(styles.CAPSIZES)
        caps = sorted(styles.CAPSIZES[:len(xss)], reverse=True)
        return [Series(x=xs, y=ys, yerrs=get_errors(ys, **yerr), name=sn, plotstyle=ps, plotparams=plotparams, capsize=cap)
                for xs, ys, yerr, ps, sn, cap in zip(xss, yss, errs, plotstyles, names, caps)]
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
                 capsize=None,
                 **kwargs):
        assert series is None or (x is not None and y is not None)
        if series is None:
            self.series = pd.Series(data=y, index=x, name=name, **kwargs)
        else:
            self.series = series
            if name is not None:
                self.series.name = name
        if yerrs is not None:
            # Assert that dimensions are either N or 2xN
            assert len(yerrs) == len(self.series) or len(yerrs[0]) == len(self.series)
        if isinstance(plotstyle, str):
            plotstyle = styles.SERIES[plotstyle]
        self.plotstyle = plotstyle
        self.yerrs = yerrs
        self.plotparams = dict(plotparams)
        if capsize is not None:
            self.plotparams['capsize'] = capsize

    def plot(self, *args, **kwargs):
        if self.plotparams is not None:
            kwargs.update(self.plotparams)
        for k in ['marker', 'color', 'label']:
            if self.plotstyle and k in self.plotstyle:
                kwargs[k] = self.plotstyle[k]
        if self.yerrs is not None:
            kwargs['yerr'] = self.yerrs
            ax = kwargs.pop('ax')
            # Pandas Series plotting with asymmetrical errorbars fix still hasn't been merged in yet
            # https://github.com/pandas-dev/pandas/issues/9536
            # https://github.com/kleingeist/pandas/commit/89f3d984ca01100c039cece36aee20569fa60483
            ax.errorbar(self.x, self.y, **kwargs)
        else:
            self.series.plot(*args, **kwargs)

    @property
    def x(self):
        return self.series.index

    @property
    def y(self):
        return self.series.values

    def __repr__(self):
        return str(self.series)