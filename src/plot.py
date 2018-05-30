import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate
from plotutils import Series


def _grid_apply(x_or_y, series, grid, ax=None):
    if grid is not None:
        if x_or_y == 'x':
            pts = [s_.x for s_ in series] if len(series) > 0 else None
        else:
            pts = [s_.y for s_ in series] if len(series) > 0 else None
        grid(pts, ax=ax)


def _order_y(series):
    """Reorder series by which has the most no of points on top (rank)"""
    df = reduce(lambda left, right: pd.merge(left, right, left_index=True, right_index=True),
                [s_.series.to_frame() for s_ in series])
    order = list(df.rank(axis=1).mean().sort_values(ascending=False).index)
    return order


def variants(series, ax=None,
             xgrid=None, ygrid=None,
             legend=None,
             order=None,
             plot_kwargs={}, legend_kwargs={}):
    """Comparing different variants of Mainstream"""
    if ax is None:
        _, ax = plt.subplots()
    if order == 'y':
        # Reorder series
        order = _order_y(series)
        series = sorted(series, key=lambda s: order.index(s.name))
    for line in series:
        line.plot(ax=ax, **plot_kwargs)
    _grid_apply('x', series, xgrid, ax=ax)
    _grid_apply('y', series, ygrid, ax=ax)
    assert legend is None or len(legend_kwargs) == 0, "Use either legend or legend_kwargs"
    if legend is None:
        ax.legend(**legend_kwargs)
    else:
        legend(ax)
    plt.tight_layout()
    return ax


def variants_dual(seriesA, seriesB,
                  xgrid=None, ygrid=None, ygrid2=None,
                  plot_kwargs={}, legend_kwargs={}):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    # # Prune biggest tick to avoid overlap
    # def ygrid2_(*args, **kwargs):
    #     kwargs['ticker_kwargs'] = dict(prune='lower')
    #     ygrid2(*args, **kwargs)
    variants(seriesA, ax=ax1, ygrid=ygrid, plot_kwargs=plot_kwargs)
    variants(seriesB, ax=ax2, ygrid=ygrid2, plot_kwargs=plot_kwargs)
    _grid_apply('x', seriesA, xgrid, ax=ax1)
    ax2.legend(**legend_kwargs)
    plt.tight_layout()
    return ax1, ax2


def frontier(series, voting_train_f1_hack=False):
    all_pts = []
    for s_ in series:
        all_pts += list(zip(s_.x, s_.y))
    pts = []
    highest = -1
    for x, y in sorted(all_pts, reverse=True):
        if y > highest:
            highest = y
            pts.append((x, y))
    pts = sorted(pts)
    xs, ys = zip(*pts)

    all_xs = [pt[0] for pt in all_pts]

    xss = np.linspace(min(all_xs), max(all_xs), 100)

    if voting_train_f1_hack:
        xs_l = list(xs)
        ys_l = list(ys)
        idx = xs_l.index(9)
        xs_l.pop(idx)
        ys_l.pop(idx)
        spl = scipy.interpolate.PchipInterpolator(xs_l, ys_l)
    else:
        spl = scipy.interpolate.PchipInterpolator(xs, ys)
    ys = spl(xss)
    return Series(x=xss, y=ys,
                  name='Frontier',
                  plotstyle={'label': 'Pareto Frontier', 'color': 'blue'},
                  plotparams={'lw': 3, 'ls': '--'})
