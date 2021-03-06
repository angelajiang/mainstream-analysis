import matplotlib.pyplot as plt
import matplotlib.ticker as plticker
from utils import flatten


grid_kwargs = dict(linestyle='dotted', linewidth=.1, axis='y')


def recall(ys, ax=None):
    ratio(ys, title="Average Event Recall", ax=ax)


def recall_zoomed(ys, ax=None):
    ratio(ys, title="Event Recall", ax=ax)
    min_y = min(flatten(ys))
    if min_y >= .5:
        ax.set_ylim(.5, 1)


def precision(ys, ax=None):
    ratio(ys, title="Average Event Precision", ax=ax)


def f1(ys, ax=None):
    ratio(ys, title="Average Event F1", ax=ax)


def accuracy(ys, ax=None):
    ratio(ys, title="Top-1 Accuracy", ax=ax)


def ratio(ys, title="??", ax=None):
    if ax is None:
        ax = plt.gca()
    ax.set_ylim(0, 1)
    ax.set_ylabel(title)


def fps(ys, label="FPS", ax=None, ticker_kwargs={}):
    if ax is None:
        ax = plt.gca()
    ax.yaxis.set_major_locator(plticker.MaxNLocator(nbins=4, integer=True, **ticker_kwargs))
    ax.set_ylim(0, max(20, max(flatten(ys))))
    ax.set_ylabel(label)


__all__ = {
    'recall': recall,
    'precision': precision,
    'f1': f1,
    'fps': fps,
}


def get(idx):
    return __all__[idx]
