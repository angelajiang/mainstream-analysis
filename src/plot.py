import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate


def _grid_apply(x_or_y, series, grid, ax=None):
    if grid is not None:
        if x_or_y == 'x':
            pts = [s_.x() for s_ in series] if len(series) > 0 else None
        else:
            pts = [s_.y() for s_ in series] if len(series) > 0 else None
        grid(pts, ax=ax)


def variants(series, ax=None,
             xgrid=None, ygrid=None,
             plot_kwargs={}, legend_kwargs={}):
    """Comparing different variants of Mainstream"""
    if ax is None:
        _, ax = plt.subplots()
    for line in series:
        line.plot(ax=ax, **plot_kwargs)
    _grid_apply('x', series, xgrid, ax=ax)
    _grid_apply('y', series, ygrid, ax=ax)
    ax.legend(**legend_kwargs)
    return ax


def variants_dual(seriesA, seriesB,
                  xgrid=None, y1grid=None, y2grid=None,
                  plot_kwargs={}, legend_kwargs={}):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    variants(seriesA, ax=ax1, xgrid=xgrid, ygrid=y1grid, plot_kwargs=plot_kwargs)
    variants(seriesB, ax=ax2, ygrid=y2grid, plot_kwargs=plot_kwargs)
    ax2.legend(**legend_kwargs)
    return ax1, ax2


# TODO: Adapt for new framework.
# def frontier(all_pts, voting_train_f1=None):
#     pts = []
#     highest = -1
#     for x, y in sorted(all_pts, reverse=True):
#         if y > highest:
#             highest = y
#             pts.append((x, y))
#     pts = sorted(pts)
#     xs, ys = zip(*pts)

#     all_xs = [pt[0] for pt in all_pts]

#     xss = np.linspace(min(all_xs), max(all_xs), 100)

#     if voting_train_f1:
#         xs_l = list(xs)
#         ys_l = list(ys)
#         for i in range(len(xs_l)):
#             if xs_l[i] == 9:
#                 to_delete = ys_l[i]
#                 xs_l = [x for x in xs if x != 9]
#                 ys_l = [y for y in ys if y != to_delete]
#                 break
#         spl = scipy.interpolate.PchipInterpolator(xs_l, ys_l)
#     else:
#         spl = scipy.interpolate.PchipInterpolator(xs, ys)
#     ys = spl(xss)
#     return xss, ys
