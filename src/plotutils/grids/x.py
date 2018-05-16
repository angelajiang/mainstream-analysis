import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator


def num_apps(xs, ax=None):
    if ax is None:
        ax = plt.gca()
    xs = set(x for xss in xs for x in xss)
    ax.set_xlim(max(min(xs), 2), max(xs))
    ax.xaxis.set_major_locator(MaxNLocator(integer=True))
    ax.set_xlabel("Number of concurrent apps")


def budget(xs, ax=None):
    if ax is None:
        ax = plt.gca()
    ax.set_xlabel("Budget")
    raise NotImplementedError
