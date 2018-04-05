import os
import math
import matplotlib
import numpy as np
import sys

sys.path.append("scripts/util")
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

import seaborn as sns

sns.set_style("white", {
              "font.family": "serif",
              "font.serif": ["Times", "Palatino", "serif"] })

def fn_inner(x, exponent, c0, c1, c2):
    val = 1 - math.pow(x, exponent)
    y = c2 * math.pow(val, 1. / exponent) + c1*(x) + c0
    return y

def fn(x, exponent, c0, eps, max_acc, num_frozen):
    assert max_acc <= 1
    c1 = eps - c0
    c2 = max_acc - c0
    scaled_x = x / float(num_frozen)

    limit_y = fn_inner(scaled_x, exponent, c0, c1, c2)

    y = fn_inner(scaled_x, exponent, c0, c1, c2)
    return y

def plot_range(exponent, c0, eps, max_acc, num_frozen):
    xs = range(0, num_frozen+1)
    ys = [fn(x, exponent, c0, eps, max_acc, num_frozen) for x in xs]
    plt.plot(xs, ys) #, label = str(c0) + "," + str(eps) + "," + str(max_acc))

def run(exponent_range, num_frozen, plot_dir):
    #exponents = range(8, exponent_range + 2, 2)
    #c0s = np.arange(0, 0.2, 0.05)

    epses = np.arange(0, 0.4, 0.1)
    max_accs = np.arange(0.4, 1, 0.2)

    exponent = 10
    c0 = 0.1

    #epses = [epses[1]]
    #max_accs = [max_accs[1]]

    for eps in epses:
        for max_acc in max_accs:
            plot_range(exponent, c0, eps, max_acc, num_frozen)
    plot_file = os.path.join(plot_dir, "variants")
    plot_util.format_plot("Number of frozen layers", "Top-1 Accuracy")
    plt.ylim(0, 1)
    plt.savefig(plot_file)
    plt.clf()

def main():
    plot_dir = "plots/goodness/accuracy_synthetic"
    run(9, 84, plot_dir)

if __name__ == "__main__":
    main()


