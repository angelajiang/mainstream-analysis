import pprint as pp
import sys
import matplotlib
import numpy as np
from itertools import cycle

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def get_data(csv_file):
    xs = []
    ys = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            stride = int(vals[0])
            prob = float(vals[1])
            xs.append(stride)
            ys.append(prob)
    return zip(*sorted(zip(xs, ys)))

def plot(rate_files, labels, plot_file):
    # xs: stride
    # ys: probability
    # Each line is a model
    cycol = cycle('rcgkmbr').next
    for rate_file, label in zip(rate_files, labels):
        xs, ys = get_data(rate_file)
        plt.plot(xs, ys, label=label+" frozen", lw=2, color=cycol())

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.xlabel("Stride", fontsize=25)
    plt.ylabel("Probability of detection", fontsize=25)
    plt.legend(loc=4, fontsize=15)
    plt.tight_layout()

    plt.savefig(plot_file)
    plt.clf()

if __name__ == "__main__":
    f1 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afp-4"
    f2 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afp-10"
    f3 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afp-14"
    plot_file = "plots/frame-rate/frame-rate-afp.pdf"
    #plot([f1, f2, f3], ["AFP-4", "AFP-10", "AFP-14"], plot_file)

    f1 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afn-0"
    f2 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afn-4"
    f3 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afn-17"
    f4 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afn-18"
    f5 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afn-41"
    f6 = "/Users/angela/src/private/mainstream/log/frame-rate/frame-rate-trains-no-afn-87"
    plot_file = "plots/frame-rate/frame-rate-afn.pdf"
    plot([f1, f2, f3, f4, f5, f6], ["0", "4", "16", "18", "41", "87"], plot_file)

