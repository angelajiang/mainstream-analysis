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


def frozen(xs, label="% of layers that are unspecialized", ax=None):
    if ax is None:
        ax = plt.gca()
    ax.set_xlabel(label)
    ax.set_xlim(0, 100)


def frozen_shared(xs, ax=None):
    frozen(xs, ax=ax, label='% of layers that are unspecialized (shared)')
    ax.set_xlim(0, 115)
