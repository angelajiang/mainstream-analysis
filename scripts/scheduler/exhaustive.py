import os
import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np

sys.path.append("scripts/util")
import plot_util
import data_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def plot_exhaustive_v0(ms_files, label_prefixes, plot_file, plot_dir):
    colors = plot_util.COLORLISTS[len(ms_files)]
    markers = plot_util.MARKERS

    metric = "F1"
    title = "F1"

    width = 0.35

    for j in range(2):

        lines = []
        all_pts = []

        for i, (ms_file, label_prefix, c) in enumerate(zip(ms_files, label_prefixes,  colors)):
            xs, ys, fpses, labels = data_util.get_exhaustive_data(ms_file)
            xs_bar = [x + (i * width) for x in xs]
            plt.bar(xs_bar, ys, width,
                            color=c,
                            alpha=0.5,
                            label = label_prefix)

        plot_util.format_plot("Config ID", "Event " + title)

        plt.ylim(0,1)

        filename = os.path.join(plot_dir, plot_file + "-" + metric)

        plt.legend(loc=3, fontsize=15)
        plt.savefig(filename + ".pdf")

        plt.clf()
