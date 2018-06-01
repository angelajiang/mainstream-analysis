
import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from itertools import cycle
from scipy.stats import linregress, stats

sys.path.append("scripts/util")
import plot_util

import seaborn as sns
sns.set_style("whitegrid")

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()


def plot_map(csv_file, plot_file, ylim, title):
    data = {}
    xs = []
    ys = []
    errs = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            trial = int(vals[0])
            num_frozen = int(vals[1])
            mAP = round(float(vals[2]),3)
            precision = round(float(vals[3]),3)
            recall = round(float(vals[4]),3)

            if num_frozen not in data.keys():
                data[num_frozen] = []
            data[num_frozen].append(mAP)

    for num_frozen, mAPs in sorted(data.items()):
        for mAP in mAPs:
            xs.append(num_frozen)
            ys.append(mAP)

    plt.scatter(xs, ys, marker=plot_util.MAINSTREAM['marker'],
                        color=plot_util.NO_SHARING['color'])

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel("Number Frozen", fontsize=30)
    plt.ylabel("mAP", fontsize=30)
    plt.title(title, fontsize=35)

    plt.ylim(0, ylim)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.savefig(plot_file)
    plt.clf()

def plot_f1(csv_file, plot_file, ylim, title):
    data = {}
    xs = []
    ys = []
    errs = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            trial = int(vals[0])
            num_frozen = int(vals[1])
            mAP = round(float(vals[2]),3)
            precision = round(float(vals[3]),3)
            recall = round(float(vals[4]),3)
            if precision != 0 and recall != 0:
                f1 = stats.hmean([precision, recall])

                if num_frozen not in data.keys():
                    data[num_frozen] = []
                data[num_frozen].append(recall)

    for num_frozen, f1s in sorted(data.items()):
        xs.append(num_frozen)
        ys.append(max(f1s))

    plt.scatter(xs, ys, marker=plot_util.MAINSTREAM['marker'],
                        color=plot_util.NO_SHARING['color'])


    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)


    plt.xlabel("Number Frozen", fontsize=30)
    plt.ylabel("Max F1", fontsize=30)
    plt.title(title, fontsize=35)

    plt.ylim(0, ylim)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.savefig(plot_file)
    plt.clf()

if __name__ == "__main__":
    plot_dir = "plots/bb/urban-tracker"

    ms_file = "output/bb/urban-tracker/v1/urban-tracker-stmarc-pedestrian"
    plot_file = plot_dir + "/v1/mAP-stmarc-pedestrian-trials.pdf"
    title = "St Marc pedestrian"
    plot_map(ms_file, plot_file, 1, title)

    ms_file = "output/bb/urban-tracker/v1/urban-tracker-stmarc-car"
    plot_file = plot_dir + "/v1/mAP-stmarc-car-trials.pdf"
    title = "St Marc car"
    plot_map(ms_file, plot_file, 1, title)

    ms_file = "output/bb/urban-tracker/v1/urban-tracker-stmarc-pedestrian"
    plot_file = plot_dir + "/v1/f1-max-stmarc-pedestrian-trials.pdf"
    title = "St Marc pedestrian"
    plot_f1(ms_file, plot_file, 1, title)

    ms_file = "output/bb/urban-tracker/v1/urban-tracker-stmarc-car"
    plot_file = plot_dir + "/v1/f1-max-stmarc-car-trials.pdf"
    title = "St Marc car"
    plot_f1(ms_file, plot_file, 1, title)
