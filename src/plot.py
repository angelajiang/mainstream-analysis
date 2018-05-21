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


def variants(series, ax=None,
             xgrid=None, ygrid=None,
             legend=None,
             plot_kwargs={}, legend_kwargs={}):
    """Comparing different variants of Mainstream"""
    if ax is None:
        _, ax = plt.subplots()
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
    variants(seriesA, ax=ax1, xgrid=xgrid, ygrid=ygrid, plot_kwargs=plot_kwargs)
    variants(seriesB, ax=ax2, ygrid=ygrid2, plot_kwargs=plot_kwargs)
    ax2.legend(**legend_kwargs)
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
                  plotstyle={'label': 'Pareto Frontier', 'color': 'blue'},
                  plotparams={'lw': 3, 'ls': '--'})
