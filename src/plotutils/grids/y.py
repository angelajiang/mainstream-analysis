import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


def recall(ys, ax=None):
    ratio(ys, title="Average Event Recall", ax=ax)


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
    ax.grid(linestyle='dotted', linewidth=.1)
    ax.set_ylabel(title)


def fps(ys, label="FPS", ax=None):
    if ax is None:
        ax = plt.gca()
    ys = set(y for yss in ys for y in yss)
    ax.yaxis.set_major_locator(plticker.MultipleLocator(base=4.))
    ax.set_ylim(0, max(20, max(ys)))
    ax.grid(None)
    ax.set_ylabel(label)


__all__ = {
    'recall': recall,
    'precision': precision,
    'f1': f1,
    'fps': fps,
}


def get(idx):
    return __all__[idx]
