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

def plot(csv_file, max_file, min_file):
    xs1 = []
    ys1 = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            fnr = float(vals[1])
            xs1.append(num_apps)
            ys1.append(fnr)

    xs2 = []
    ys2 = []
    with open(max_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            fnr = float(vals[1])
            xs2.append(num_apps)
            ys2.append(fnr)

    xs3 = []
    ys3 = []
    with open(min_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            fnr = float(vals[1])
            xs3.append(num_apps)
            ys3.append(fnr)

    plt.plot(xs1, ys1, marker="o", lw=2, label="Mainstream")
    plt.plot(xs2, ys2, marker="h", lw=2, label="Max sharing")
    plt.plot(xs3, ys3, marker="D", lw=2, label="No sharing")

    plt.legend(loc=0)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel("Number of apps", fontsize=25)
    plt.ylabel("False negative rate", fontsize=25)
    plt.xlim(1, 15)
    plt.tight_layout()
    plt.show()
    plt.savefig("plots/scheduler/scheduler.pdf")
    plt.clf()

if __name__ == "__main__":
    csv_file = "output/streamer/scheduler/scheduler-s0.3-app15.csv" 
    max_file = "output/streamer/scheduler/scheduler-s0.3-app15-max.csv" 
    min_file = "output/streamer/scheduler/scheduler-s0.3-app15-min.csv" 
    plot(csv_file, max_file, min_file)
