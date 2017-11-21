
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
    data = {"hybrid": {"xs": [], "ys": []}, "split": {"xs": [], "ys": []}}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            version = vals[0]
            num_frozen = int(vals[1])
            mAP = round(float(vals[2]),3)
            data[version]["xs"].append(num_frozen)
            data[version]["ys"].append(mAP)

    colors = [plot_util.MAINSTREAM['color'], plot_util.MAX_SHARING['color']]

    for (version, d), c in zip(data.iteritems(), colors):

        plt.plot(d["xs"], d["ys"], marker=plot_util.MAINSTREAM['marker'], lw=2, color=c, label=version)

        plt.tick_params(axis='y', which='major', labelsize=28)
        plt.tick_params(axis='y', which='minor', labelsize=20)
        plt.tick_params(axis='x', which='major', labelsize=28)
        plt.tick_params(axis='x', which='minor', labelsize=20)
        plt.legend()

        plt.xlabel("Number Frozen", fontsize=35)
        plt.ylabel("mAP", fontsize=35)

    plt.tight_layout()
    plt.grid()
    plt.savefig(plot_dir + "/mAP.pdf")

if __name__ == "__main__":
    plot_dir = "plots/bb/"
    ms_file = "output/bb/mAP.csv"
    plot(ms_file, plot_dir)


