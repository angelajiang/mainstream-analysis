
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

def get_data(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            line = line.rstrip('\n')
            vals = line.split(',')
            num_frozen = int(vals[0])
            mAP = round(float(vals[1]),3)
            precision = round(float(vals[2]),3)
            recall = round(float(vals[3]),3)
            model_name = vals[4]

            if precision == 0 or recall == 0:
                continue

            f1 = stats.hmean([precision, recall])

            if num_frozen not in data.keys():
                data[num_frozen] = {"maps":[], "f1s": [], "model_names": []}

            data[num_frozen]["maps"].append(mAP)
            data[num_frozen]["f1s"].append(f1)
            data[num_frozen]["model_names"].append(model_name)
    return data

def plot_model_set(csv_file, plot_prefix, title, setfile):
    '''
    Plot mAP and F1 for monotonically ascending values of max(f1s)
    '''

    data_by_num_frozen = get_data(csv_file)

    xs = []
    y_maps = []
    y_f1s = []

    prev_max_f1 = -1

    with open(set_file, "w+") as f:

        for num_frozen, data in reversed(list(sorted(data_by_num_frozen.items()))):
            maps = data["maps"]
            f1s = data["f1s"]
            model_names = data["model_names"]

            i = np.argmax(model_names)
            model_name = model_names[i]
            max_map = max(maps)
            max_f1 = max(f1s)

            if max_f1 > prev_max_f1:
                xs.append(num_frozen)
                y_maps.append(max_map)
                y_f1s.append(max_f1)

                line = "%d,%.6g,%s\n" % (num_frozen,
                                              max_f1,
                                              model_name)
                f.write(line)

                prev_max_f1 = max_f1

    xlabel = "Number Frozen"
    ylabel = "mAP"
    plot_file = plot_prefix + "-model-set-mAP.pdf"
    plot(xs, y_maps, xlabel, ylabel, plot_file)

    print plot_file

    ylabel = "F1-score"
    plot_file = plot_prefix + "-model-set-F1.pdf"
    plot(xs, y_f1s, xlabel, ylabel, plot_file)

    print plot_file
    print set_file

def plot_model_superset(csv_file, plot_prefix, title):
    '''
    Plot mAP and F1 for all trials
    '''

    data_by_num_frozen = get_data(csv_file)

    xs = []
    y_maps = []
    y_f1s = []

    for num_frozen, data in sorted(data_by_num_frozen.items()):
        maps = data["maps"]
        f1s = data["f1s"]

        for m, f in zip(maps, f1s):
            xs.append(num_frozen)
            y_maps.append(m)
            y_f1s.append(f)

    xlabel = "Number Frozen"
    ylabel = "mAP"
    plot_file = plot_prefix + "-model-superset-mAP.pdf"
    plot(xs, y_maps, xlabel, ylabel, plot_file)

    ylabel = "F1-score"
    plot_file = plot_prefix + "-model-superset-F1.pdf"
    plot(xs, y_f1s, xlabel, ylabel, plot_file)


def plot(xs, ys, xlabel, ylabel, plot_file):

    plt.scatter(xs, ys, marker=plot_util.MAINSTREAM['marker'],
                        color=plot_util.NO_SHARING['color'])

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel(xlabel, fontsize=30)
    plt.ylabel(ylabel, fontsize=30)
    plt.title(title, fontsize=35)

    plt.ylim(0, 1)
    plt.legend()
    plt.tight_layout()
    plt.grid()
    plt.savefig(plot_file)
    plt.clf()

if __name__ == "__main__":
    plot_dir = "plots/bb/urban-tracker/v2/"

    ms_file = "output/bb/urban-tracker/v2/urban-tracker-stmarc-pedestrian"
    plot_prefix = plot_dir + "stmarc-pedestrian"
    title = "St Marc Pedestrian"
    set_file = "output/mainstream/f1/pedestrians/stmarc-pedestrian-set"
    plot_model_set(ms_file, plot_prefix, title, set_file)
    plot_model_superset(ms_file, plot_prefix, title)

