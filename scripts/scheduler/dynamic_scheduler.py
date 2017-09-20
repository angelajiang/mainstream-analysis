import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from itertools import cycle
from scipy.stats import linregress
sys.path.append("scripts/util")
import plot_util


matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def plot(csv_file, plot_dir):
    data = {}
    thresholds = [2, 4, 6, 8]
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            threshold = float(vals[1])
            if threshold in thresholds:
                err = float(vals[2])
                stdev = float(vals[4])
                num_frozen_list = [float(v) for v in vals[4:]]
                if threshold not in data.keys():
                    data[threshold] = {"xs":[], "ys":[]}

                data[threshold]["xs"].append(num_apps)
                data[threshold]["ys"].append(err)

    labels = []

    # Plot accuracy on the y axis
    colors = plot_util.COLORLISTS[4]
    markers = ["o", "h", "D", "p", "8", "x", "1"]

    Xs = data[thresholds[0]]["xs"]
    Ys = [.174] * len(Xs)
    plt.plot(Xs, Ys, color="black", lw=2, marker="*", markersize=10)
    labels.append("Max sharing")

    count = 0
    color_index = 0
    for threshold, vals in reversed(sorted(data.iteritems())):
        color = colors[color_index]
        Xs = vals["xs"]
        Ys = vals["ys"]
        plt.plot(Xs, Ys, color=color, lw=2, marker=markers[count], markersize=10)
        labels.append(str(int(threshold)) + " fps")
        count += 1
        color_index += 1

    plt.legend(labels, loc=0)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlim(1,10)
    plt.xlabel("Number of applications", fontsize=25)
    plt.ylabel("Image-level Accuracy Loss", fontsize=25)
    plt.tight_layout()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)
    plt.savefig(plot_dir + "/dynamic-scheduler-uniform.pdf")
    plt.clf()

if __name__ == "__main__":
    csv_file = "output/streamer/scheduler/dynamic-uniform.csv" 
    plot_dir = "plots/scheduler/"


    plot(csv_file, plot_dir)
