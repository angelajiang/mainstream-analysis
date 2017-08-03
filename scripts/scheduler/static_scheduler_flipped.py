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

def plot(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            threshold = float(vals[1])
            fps = float(vals[2])
            err = float(vals[3])

            if num_apps not in data.keys():
                data[num_apps] = {}

            data[num_apps][threshold] = fps

    plot_data = {}
    for fps in range(1, 10):
        plot_data[fps] = {"xs": [], "ys":[]}
        for num_apps in sorted(data.keys()):
            min_acc = float("inf")
            for acc in data[num_apps].keys():
                if data[num_apps][acc] > fps and acc < min_acc:
                    min_acc = acc
            if min_acc != float("inf"):
                plot_data[fps]["xs"].append(num_apps)
                plot_data[fps]["ys"].append(min_acc)


    labels = []
    cycol = cycle('bgrcmyk').next
    for fps, vals in plot_data.iteritems():

        Xs = vals["xs"]
        Ys = vals["ys"]

        plt.plot(Xs, Ys, lw=2, color=cycol())
        labels.append(str(fps) + " fps")

    plt.legend(labels, loc=0, ncol=2)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel("Number of apps", fontsize=20)
    plt.ylabel("Relative accuracy", fontsize=20)
    plt.yscale("log")
    plt.tight_layout()
    plt.savefig("plots/scheduler/static-scheduler-flipped.pdf")
    plt.clf()


if __name__ == "__main__":
    csv_file = sys.argv[1]
    plot(csv_file)
