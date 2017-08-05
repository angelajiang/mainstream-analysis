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
            #err = math.floor(float(vals[3]) * 1000) / 1000
            err = float(vals[2]) * num_apps
            stdev = float(vals[4])
            num_frozen_list = [float(v) for v in vals[4:]]
            if threshold not in data.keys():
                data[threshold] = {"xs":[], "ys":[]}

            data[threshold]["xs"].append(num_apps)
            data[threshold]["ys"].append(err)

    labels = []

    # Plot accuracy on the y axis
    cycol = cycle('bgrcmyk').next
    for threshold, vals in data.iteritems():
        print threshold, vals
        Xs = vals["xs"]
        Ys = vals["ys"]
        plt.plot(Xs, Ys, color=cycol(), lw=2)
        labels.append(str(int(threshold)) + " fps")

    plt.legend(labels, loc=0)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel("Number of apps", fontsize=20)
    plt.ylabel("Sum rel acc loss", fontsize=20)
    plt.tight_layout()
    plt.savefig("plots/scheduler/dynamic-scheduler.pdf")
    plt.clf()

if __name__ == "__main__":
    csv_file = sys.argv[1]
    plot(csv_file)