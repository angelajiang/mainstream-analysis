import matplotlib.pyplot as plt
import matplotlib.ticker as ticker
import math


def num_apps(xs, ax=None):
    if ax is None:
        ax = plt.gca()
    xs = set(x for xss in xs for x in xss)
    ax.set_xlim(max(min(xs), 2), max(xs))
    ax.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))
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


def _fraction_log_fmt(x, _):
    if x >= 1:
        return '{:g}'.format(x)
    else:
        return '$\\frac{{1}}{{{:g}}}$'.format(1. / x)


def sample_rate(xs, ax=None):
    ax.set_xlabel("Frame sample rate")
    min_x = min(x for xss in xs for x in xss)
    # ax.set_xlim(pow(10, math.floor(math.log10(min_x))), 1)
    ax.set_xscale("log")
    ax.xaxis.set_major_formatter(ticker.FuncFormatter(_fraction_log_fmt))
