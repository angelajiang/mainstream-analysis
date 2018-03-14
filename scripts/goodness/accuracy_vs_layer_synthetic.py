import os
import math
import matplotlib
import sys

sys.path.append("scripts/util")
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def fn(x, exponent, num_frozen):
    val = 1  - math.pow(x / float(num_frozen), exponent)
    y = math.pow(val, 1. / exponent)
    return y

def plot_range(exponent, num_frozen):
    xs = range(0, num_frozen)
    ys = [fn(x, exponent, num_frozen) for x in xs]
    plt.plot(xs, ys) 

def run(exponent_range, num_frozen, plot_dir):
    exponents = range(1, exponent_range)
    for exponent in exponents:
        plot_range(exponent, num_frozen)
    plot_file = os.path.join(plot_dir, "accuracy-synthetic-"+str(exponent_range)+".pdf")
    plot_util.format_plot("Number of concurrent apps", "F1-score")
    plt.savefig(plot_file)

def main():
    plot_dir = "plots/accuracy/"
    run(20, 84, plot_dir)

if __name__ == "__main__":
    main()


