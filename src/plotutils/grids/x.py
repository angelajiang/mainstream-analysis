import matplotlib.pyplot as plt


def num_apps(xs, ax=None):
    if ax is None:
        ax = plt.gca()
    xs = set(x for xss in xs for x in xss)
    ax.set_xlim(max(min(xs), 2), max(xs))
    ax.set_xlabel("No of apps")
