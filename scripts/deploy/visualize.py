
import pprint as pp
import sys
import matplotlib
import numpy as np

sys.path.append("scripts/util")
import plot_util

import matplotlib.pyplot as plt


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
        plt.scatter(xs[40:80], ys[40:80],
                    label=obj["label"],
                    color=obj["color"],
                    marker = obj["marker"])
    print ys[140:160]
    plot_file = plot_dir + "/deploy-time-series.pdf"
    plt.legend()
    plt.savefig(plot_file)

if __name__ == "__main__":
    # Data created by mainstream analyze_deployment
    # Format: frame_id, is_analyzed
    f0 = "output/streamer/deploy/flowers/6apps-independent-nosharing"
    f1 = "output/streamer/deploy/flowers/6apps-independent-maxsharing"
    f2 = "output/streamer/deploy/flowers/6apps-independent-mainstream"
    plot_dir = "plots/deploy"
    files = [f0, f1, f2]
    files = [f2]
    objs = [plot_util.NO_SHARING, plot_util.MAX_SHARING, plot_util.MAINSTREAM]
    visualize_deployment(files, objs, plot_dir)
