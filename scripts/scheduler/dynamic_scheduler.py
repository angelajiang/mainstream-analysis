import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from itertools import cycle
from scipy.stats import linregress


matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def plot(csv_file, plot_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            threshold = float(vals[1])
            if threshold in [2, 4, 6, 8]:
                err = float(vals[2])
                stdev = float(vals[4])
                num_frozen_list = [float(v) for v in vals[4:]]
                if threshold not in data.keys():
                    data[threshold] = {"xs":[], "ys":[]}

                data[threshold]["xs"].append(num_apps)
                data[threshold]["ys"].append(err)

    labels = []

    # Plot accuracy on the y axis
    cycol = cycle('bgrcmyk').next
    shapes = ["o", "h", "D", "x", "1", "*", "P", "8"]
    index = 0
    for threshold, vals in data.iteritems():
        print threshold, vals
        Xs = vals["xs"]
        Ys = vals["ys"]
        shape = shapes[index]
        plt.plot(Xs, Ys, color=cycol(), lw=2, marker=shape)
        labels.append(str(int(threshold)) + " fps")
        index += 1

    Ys = [.174] * len(Xs)
    shape = shapes[index]
    plt.plot(Xs, Ys, color="black", lw=2, marker=shape)
    labels.append("Max sharing")

    plt.legend(labels, loc=0)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel("Number of apps", fontsize=25)
    plt.ylabel("Avg Relative Top-1 Acc Loss", fontsize=25)
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.clf()

if __name__ == "__main__":
    csv_file = "output/streamer/scheduler/dynamic-uniform.csv" 
    plot_file = "plots/scheduler/dynamic-scheduler-uniform.pdf"
    plot(csv_file, plot_file)
