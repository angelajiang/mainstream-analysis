
import pprint as pp
import sys
import matplotlib
import numpy as np

sys.path.append("scripts/util")
import plot_util

import matplotlib.pyplot as plt

import matplotlib
matplotlib.rcParams['mathtext.fontset'] = 'stix'
matplotlib.rcParams['font.family'] = 'STIXGeneral'

def visualize_deployment(files, objects, plot_dir):
    for csv_file, obj in zip(files, objects):
        xs = []
        ys = []
        with open(csv_file) as f:
            for line in f:
                vals = line.split(',')
                frame_id = int(vals[0])
                is_analyzed = int(vals[1])
                xs.append(frame_id)
                ys.append(is_analyzed)
        start = 7700
        end = 7800
        plt.scatter(xs[start:end], ys[start:end],
                    label=obj["label"] + " samples",
                    color=obj["color"],
                    marker = obj["marker"])
    plot_file = plot_dir + "/deploy-time-series.pdf"
    plt.title("Train detector w/ 19 apps", fontsize=30)
    plt.xlabel("Time ->", fontsize=28)
    plt.yticks([0,1], ["No Hit", "Hit"], fontsize=23, rotation='vertical')
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.legend(loc=7, fontsize=15, ncol=1)
    plt.savefig(plot_file)

if __name__ == "__main__":
    # Data created by mainstream analyze_deployment
    # Format: frame_id, is_analyzed
    f0 = "output/streamer/deploy/train/vid5-20apps-nosharing-viz"
    f1 = "output/streamer/deploy/train/vid5-20apps-mainstream-viz"
    plot_dir = "plots/deploy"
    files = [f0, f1]
    objs = [plot_util.NO_SHARING, plot_util.MAINSTREAM]
    visualize_deployment(files, objs, plot_dir)
