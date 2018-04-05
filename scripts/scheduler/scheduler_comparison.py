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

import matplotlib.pyplot as plt

def plot_bar_v0(ms_files, label_prefixes, plot_file, plot_dir, limit=20):
    colors = plot_util.COLORLISTS[len(ms_files)]

    metric = "F1"
    title = "F1"

    width = 0.3

    for j in range(2):

        lines = []
        all_pts = []

        for i, (ms_file, label_prefix, c) in enumerate(zip(ms_files, label_prefixes,  colors)):
            metrics, fpses = data_util.get_scheduler_data(ms_file)

            ys = []
            avg_fpses = []
            for num_apps in sorted(metrics.keys()):
                ys += metrics[num_apps]
                avg_fpses += fpses[num_apps]

            xs = range(len(ys))

            xs_bar = [x + (i * width) for x in xs]
            plt.bar(xs_bar[:limit], ys[:limit], width,
                            color=c,
                            alpha=0.5,
                            label = label_prefix)

        plot_util.format_plot("Config ID", "Event " + title)

        plt.ylim(0,1)

        filename = os.path.join(plot_dir, plot_file + "-" + metric)

        plt.legend(loc=3, fontsize=15)
        plt.savefig(filename + ".pdf")

        plt.clf()

def plot_by_num_apps_v0(ms_files, labels, num_setups, plot_file, plot_dir):
    colors = plot_util.COLORLISTS[len(ms_files)]
    markers = plot_util.MARKERS

    metric = "F1"

    for j in range(2):

        lines = []
        all_pts = []

        for i, (ms_file, label, m, c) in enumerate(zip(ms_files, labels, markers, colors)):
            metrics, fpses = data_util.get_scheduler_data(ms_file)

            xs = []
            ys = []
            errs = []
            for num_apps in sorted(metrics.keys()):
                if num_setups > len(metrics[num_apps]):
                    continue
                xs.append(num_apps)
                ys.append(np.average(metrics[num_apps]))
                errs.append(np.std(metrics[num_apps]))

            plt.plot(xs, ys, label=label,
                             lw=4,
                             markersize=8,
                             alpha=0.5,
                             marker=m,
                             color=c)

            #plt.errorbar(xs, ys, yerr=errs, label=label,
            #                 lw=4,
            #                 markersize=8,
            #                 marker=m,
            #                 color=c)

        plot_util.format_plot("Num Apps", "Average Event " + metric)
        plt.title(str(num_setups) + " setups per point", fontsize=20)

        plt.ylim(0,1)

        filename = os.path.join(plot_dir, plot_file + "-" + metric)

        plt.legend(loc=0, fontsize=15)
        plt.savefig(filename + ".pdf")

        plt.clf()

def plot_latency_v0(ms_files, labels, plot_file, plot_dir):

    colors = plot_util.COLORLISTS[len(ms_files)]
    markers = plot_util.MARKERS

    for i, (ms_file, label, m, c) in enumerate(zip(ms_files, labels, markers, colors)):
        xs, ys, errs = data_util.get_performance_data(ms_file)

        plt.plot(xs, ys, label=label,
                         lw=4,
                         markersize=8,
                         alpha=0.5,
                         marker=m,
                         color=c)

        #plt.errorbar(xs, ys, yerr=errs, label=label,
        #                 lw=4,
        #                 markersize=8,
        #                 marker=m,
        #                 color=c)


    filename = os.path.join(plot_dir, plot_file)

    plot_util.format_plot("Num Apps", "Average Latency (us)", 15)

    plt.tight_layout()
    plt.yscale('log')
    plt.legend(loc=0, fontsize=15)
    plt.savefig(filename + ".pdf")

    plt.clf()

