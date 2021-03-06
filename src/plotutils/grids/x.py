import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math
from utils import flatten


def scaledsize(scale=1.):
    return mpl.rcParams['axes.labelsize'] * scale


def num_apps(xs, ax=None, ticker_kwargs={}):
    if ax is None:
        ax = plt.gca()
    xs = set(x for xss in xs for x in xss)
    ax.xaxis.set_major_locator(ticker.MaxNLocator(nbins=5, integer=True, **ticker_kwargs))
    ax.set_xlim(0, max(xs))
    ax.set_xlabel("Number of concurrent apps")


def budget(xs, ax=None):
    if ax is None:
        ax = plt.gca()
    xs = flatten(xs)
    ax.set_xlim(min(xs) - 10, max(xs) + 10)
    ax.set_xlabel("Budget")


def frozen(xs, label="% of layers that are unspecialized", ax=None):
    if ax is None:
        ax = plt.gca()
    ax.set_xlabel(label, fontsize=scaledsize(.9))
    ax.set_xlim(0, 100)


def frozen_shared(xs, ax=None):
    frozen(xs, ax=ax, label='% of layers that are unspecialized (shared)')
    ax.set_xlim(0, 128)
    ax.set_xticks(range(0, 100 + 1, 20))


def _fraction_log_fmt(x, _):
    if x >= 1:
        return '{:g}'.format(x)
    else:
        return '$\\frac{{1}}{{{:g}}}$'.format(1. / x)


def sample_rate(xs, ax=None):
    ax.set_xlabel("Frame sample rate")
    # min_x = min(flatten(xs))
    # ax.set_xlim(pow(10, math.floor(math.log10(min_x))), 1)
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(_fraction_log_fmt))
