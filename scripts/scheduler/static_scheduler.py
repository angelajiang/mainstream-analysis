import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
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
            if threshold == 0:
                label = "No sharing"
            elif threshold == 1:
                label = "Max sharing"
            else:
                label = "Within " + str(threshold)

            if label not in data.keys():
                data[label] = {"xs":[], "ys":[], "errs": []}

            data[label]["xs"].append(num_apps)
            data[label]["ys"].append(fps)
            data[label]["errs"].append(err)

    labels = []
    for label, vals in data.iteritems():

        Xs = vals["xs"]
        Ys = vals["ys"]
        errs = vals["errs"]
        plt.errorbar(Xs, Ys, yerr=errs, lw=2)
        labels.append(label)

    plt.legend(labels, loc=0)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel("Number of apps", fontsize=20)
    plt.ylabel("Throughput (fps)", fontsize=20)
    plt.tight_layout()
    plt.savefig("plots/scheduler/static-scheduler.pdf")
    plt.clf()


if __name__ == "__main__":
    csv_file = sys.argv[1]
    plot(csv_file)
