
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


def get_data(csv_file):
    costs = {}
    xs = []
    ys = []
    errs = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            acc_loss = round(float(vals[2]),2)
            fps_list = [float(v) for v in vals[(4+num_apps):]]
            average_fps = round(np.average(fps_list),2)
            cost = float(vals[-1])

            if num_apps not in costs.keys():
                xs.append(num_apps)
                costs[num_apps] = []
            costs[num_apps].append(cost)

    for x in xs:
        ys.append(np.average(costs[x]))
        errs.append(np.std(costs[x]))
    return xs, ys, errs

def plot(ms_file, plot_dir):
    xs, ys, err = get_data(ms_file)
    plt.errorbar(xs, ys, yerr=err, marker=plot_util.MAINSTREAM['marker'], lw=2, label="Mainstream")

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel("Number of applications", fontsize=35)
    plt.xlim(2, max(xs))
    plt.ylim(0, max(ys))
    plt.ylabel("Cost achieved", fontsize=35)
    plt.tight_layout()
    plt.grid()
    plt.savefig(plot_dir + "/cost.pdf")

if __name__ == "__main__":
    plot_dir = "plots/scheduler"
    ms_file = "output/streamer/scheduler/cost/scheduler-s0-250-cost-mainstream" 
    plot(ms_file, plot_dir)


