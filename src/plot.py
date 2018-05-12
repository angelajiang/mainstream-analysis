import matplotlib.pyplot as plt
import numpy as np
import scipy.interpolate


def variants(series, ax=None, plot_kwargs={}, legend_kwargs={}):
    """Comparing different variants of Mainstream"""
    if ax is None:
        ax = plt.gca()
    for line in series:
        line.plot(ax=ax, **plot_kwargs)
    ax.legend(**legend_kwargs)
    return ax


def variants_dual(seriesA, seriesB, plot_kwargs={}, legend_kwargs={}):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()
    variants(seriesA, ax1, plot_kwargs=plot_kwargs)
    variants(seriesB, ax2, plot_kwargs=plot_kwargs)
    ax2.legend(**legend_kwargs)
    return ax1, ax2


def frontier(all_pts, voting_train_f1=None):
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

    if voting_train_f1:
        xs_l = list(xs)
        ys_l = list(ys)
        for i in range(len(xs_l)):
            if xs_l[i] == 9:
                to_delete = ys_l[i]
                xs_l = [x for x in xs if x != 9]
                ys_l = [y for y in ys if y != to_delete]
                break
        spl = scipy.interpolate.PchipInterpolator(xs_l, ys_l)
    else:
        spl = scipy.interpolate.PchipInterpolator(xs, ys)
    ys = spl(xss)
    return xss, ys
