
import pprint as pp
import sys
import matplotlib
import numpy as np

sys.path.append("scripts/util")
import plot_util
from matplotlib.pyplot import text

import matplotlib.pyplot as plt
import matplotlib

import seaborn as sns
sns.set()

def visualize_deployment(files, objects, plot_dir):
    start = 50
    #end = 114
    for csv_file, obj in zip(files, objects):
        xs1 = []
        xs2 = []
        ys1 = []
        ys2 = []
        with open(csv_file) as f:
            for line in f:
                vals = line.split(',')
                frame_id = int(vals[0])
                is_analyzed = int(vals[1])
                if is_analyzed == -1 or frame_id <= start:
                    continue
                if is_analyzed == 1:
                    xs1.append(frame_id)
                    ys1.append(1)
                else:
                    xs2.append(frame_id)
                    ys2.append(1)
        plt.scatter(xs1, ys1,
                    label=obj["label"] + " hit",
                    color=obj["color"],
                    s=70,
                    marker = "x")
        plt.scatter(xs2, ys2,
                    label=obj["label"] + " miss",
                    color=obj["color"],
                    s=70,
                    marker = ">")
    train_front = 114
    plt.axvline(x= train_front, linestyle="--", color="black", alpha=0.5)
    plot_file = plot_dir + "/deploy-time-series.pdf"
    plt.title("Train detector w/ 9 apps", fontsize=30)

    plt.annotate("Train front",
                 xy=(train_front, 0.9),
                 xytext=(100, -90),
                 xycoords='data',
                 fontsize=30,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    plt.xlim(start, max(xs1))
    plt.ylim(.8, 1.1)
    plt.xlabel("Time ->", fontsize=28)
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    plt.tick_params(axis='y', which='both', left='off', top='off', labelleft='off')
    plt.legend(loc=7, fontsize=15, ncol=1, frameon=True)
    plt.savefig(plot_file)

if __name__ == "__main__":
    # Data created by mainstream analyze_deployment
    # Format: frame_id, is_analyzed
    f0 = "output/streamer/deploy/train/train2-10apps-nosharing"
    f1 = "output/streamer/deploy/train/train2-10apps-mainstream"
    f2 = "output/streamer/deploy/train/train2-10apps-maxsharing"
    plot_dir = "plots/deploy"
    files = [f0, f1]
    objs = [plot_util.NO_SHARING, plot_util.MAINSTREAM]
    visualize_deployment(files, objs, plot_dir)
