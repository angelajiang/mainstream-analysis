import os
import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from itertools import cycle
from scipy.stats import linregress, hmean
from data_util import get_recall_data, get_precision_data, get_f1_data, collect_comb_csvs

sys.path.append("scripts/util")
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()


def plot_correlation(ms_files, labels, plot_file, plot_dir, version=0):
    colors = plot_util.COLORLISTS[len(ms_files)]
    markers = plot_util.MARKERS[:len(ms_files)]
    for i in range(2):
        for ms_file, label, c, m in zip(ms_files, labels, colors, markers):
            xs, ys, errs, losses, fpses = get_recall_data(ms_file, version)
            plt.errorbar(xs, ys, yerr=errs, label=label, lw=4, markersize=8,
                         marker=m,
                         color=c)

        plot_util.format_plot("Number of concurrent apps", "Recall")
        plt.xlim(max(min(xs),2), max(xs))
        plt.ylim(0, 1)

        plt.savefig(plot_dir + "/" + plot_file + "-correlation.pdf")
        plt.clf()

def plot_x_voting(ms_files, labels, plot_file, plot_dir):
    colors = plot_util.COLORLISTS[len(ms_files)]
    markers = plot_util.MARKERS[:len(ms_files)]
    for i in range(2):
        for ms_file, label, c, m in zip(ms_files, labels, colors, markers):
            xs, ys, errs, losses, fpses = get_f1_data(ms_file)
            plt.errorbar(xs, ys, yerr=errs, label=label, lw=4, markersize=8,
                         marker=m,
                         color=c)

        plot_util.format_plot("Number of concurrent apps", "Event F1-score")
        plt.xlim(max(min(xs),2), max(xs))
        plt.ylim(0, 1)

        plt.savefig(plot_dir + "/" + plot_file + "-f1.pdf")
        plt.clf()

    for i in range(2):
        for ms_file, label, c, m in zip(ms_files, labels, colors, markers):
            xs, ys, errs, _, _ = get_recall_data(ms_file, 1)

            plt.errorbar(xs, ys, yerr=errs, label=label, lw=4, markersize=8,
                         marker=m,
                         color=c)

        plot_util.format_plot("Number of concurrent apps", "Event Recall")
        plt.xlim(max(min(xs),2), max(xs))
        plt.ylim(0, 1)

        plt.savefig(plot_dir + "/" + plot_file + "-recall.pdf")
        plt.clf()

    for i in range(2):
        for ms_file, label, c, m in zip(ms_files, labels, colors, markers):
            xs, ys, errs, _, _ = get_precision_data(ms_file)
            plt.errorbar(xs, ys, yerr=errs, label=label, lw=4, markersize=8,
                         marker=m,
                         color=c)

        plot_util.format_plot("Number of concurrent apps", "Event Precision")
        plt.xlim(max(min(xs),2), max(xs))
        plt.ylim(0, 1)

        plt.savefig(plot_dir + "/" + plot_file + "-precision.pdf")
        plt.clf()
        plt.clf()

def plot_recall(ms_files, max_files, min_files, plot_files, titles, plot_dir, version=0):
    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):
            xs1, ys1, errs1, losses1, fpses1 = get_recall_data(ms_file, version)
            xs2, ys2, errs2, losses2, fpses2 = get_recall_data(max_file, version)
            xs3, ys3, errs3, losses3, fpses3 = get_recall_data(min_file, version)

            plt.errorbar(xs3, ys3, yerr=errs3, lw=4, markersize=8,
                         marker=plot_util.NO_SHARING['marker'],
                         color=plot_util.NO_SHARING['color'],
                         label=plot_util.NO_SHARING['label'])
            plt.errorbar(xs2, ys2, yerr=errs2, lw=4, markersize=8,
                         marker=plot_util.MAX_SHARING['marker'],
                         color=plot_util.MAX_SHARING['color'],
                         label=plot_util.MAX_SHARING['label'])
            plt.errorbar(xs1, ys1, yerr=errs1, lw=4, markersize=8,
                         marker=plot_util.MAINSTREAM['marker'],
                         color=plot_util.MAINSTREAM['color'],
                         label=plot_util.MAINSTREAM['label'])

            plot_util.format_plot("Number of concurrent apps", "Event Recall")
            plt.xlim(max(min(xs1),2), max(xs1))
            plt.ylim(0, 1)

            plt.savefig(plot_dir + "/" + plot_file + "-recall.pdf")
            plt.clf()

def plot_precision(ms_files, max_files, min_files, plot_files, titles, plot_dir):
    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):
            xs1, ys1, errs1, _, _ = get_precision_data(ms_file)
            xs2, ys2, errs2, _, _ = get_precision_data(max_file)
            xs3, ys3, errs3, _, _ = get_precision_data(min_file)

            plt.errorbar(xs3, ys3, yerr=errs3, lw=4, markersize=8,
                         marker=plot_util.NO_SHARING['marker'],
                         color=plot_util.NO_SHARING['color'],
                         label=plot_util.NO_SHARING['label'])
            plt.errorbar(xs2, ys2, yerr=errs2, lw=4, markersize=8,
                         marker=plot_util.MAX_SHARING['marker'],
                         color=plot_util.MAX_SHARING['color'],
                         label=plot_util.MAX_SHARING['label'])
            plt.errorbar(xs1, ys1, yerr=errs1, lw=4, markersize=8,
                         marker=plot_util.MAINSTREAM['marker'],
                         color=plot_util.MAINSTREAM['color'],
                         label=plot_util.MAINSTREAM['label'])

            plot_util.format_plot("Number of concurrent apps", "Event Precision")
            plt.xlim(max(min(xs1),2), max(xs1))
            plt.ylim(0, 1)

            plt.savefig(plot_dir + "/" + plot_file + "-precision.pdf")
            plt.clf()

def plot_f1(ms_files, max_files, min_files, plot_files, titles, plot_dir, xlim=None, annotations = [], ms_variant_files=[], ms_variant_name=None, legend=False):
    for i in range(2):
        for i, (ms_file, max_file, min_file, plot_file, title) \
                in enumerate(zip(ms_files, max_files, min_files, plot_files, titles)):
            ms_variant_file = ms_variant_files[i] if ms_variant_files else None
            xs1, ys1, errs1, losses1, fpses1 = get_f1_data(ms_file)
            xs2, ys2, errs2, losses2, fpses2 = get_f1_data(max_file)
            xs3, ys3, errs3, losses3, fpses3 = get_f1_data(min_file)
            if ms_variant_file:
                xs4, ys4, errs4, losses4, fpses4 = get_f1_data(ms_variant_file)



            plot_util.format_plot("Number of concurrent apps", "Event F1-score")
            if xlim:
                plt.xlim(*xlim)
            else:
                plt.xlim(max(min(xs1),2), max(xs1))
            plt.ylim(0, 1)

            plt.errorbar(xs3, ys3, yerr=errs3, lw=4, markersize=8,
                         marker=plot_util.NO_SHARING['marker'],
                         color=plot_util.NO_SHARING['color'],
                         label=plot_util.NO_SHARING['label'])
            plt.errorbar(xs2, ys2, yerr=errs2, lw=4, markersize=8,
                         marker=plot_util.MAX_SHARING['marker'],
                         color=plot_util.MAX_SHARING['color'],
                         label=plot_util.MAX_SHARING['label'])
            plt.errorbar(xs1, ys1, yerr=errs1, lw=4, markersize=8,
                         marker=plot_util.MAINSTREAM['marker'],
                         color=plot_util.MAINSTREAM['color'],
                         label=plot_util.MAINSTREAM['label'])
            if ms_variant_file:
                plt.errorbar(xs4, ys4, yerr=errs4, lw=4, markersize=8,
                             marker=plot_util.MAINSTREAM_VARIANT['marker'],
                             color=plot_util.MAINSTREAM_VARIANT['color'],
                             label=ms_variant_name if ms_variant_name else plot_util.MAINSTREAM_VARIANT['label'])

            if legend:
                leg = plt.legend(loc=1)
                leg.get_frame().set_alpha(0.5)

            plt.savefig(plot_dir + "/" + plot_file + "-f1.pdf")

            if len(annotations) > 0:
                assert len(annotations) == 6

                (x, y, loss, fps) = (xs1[annotations[0]],
                                     ys1[annotations[0]],
                                     losses1[annotations[0]],
                                     fpses1[annotations[0]])
                plt.annotate("Frame Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x, y),
                             xytext=(20, 30),
                             xycoords='data',
                             fontsize=15,
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

                (x, y, loss, fps) = (xs1[annotations[1]],
                                     ys1[annotations[1]],
                                     losses1[annotations[1]],
                                     fpses1[annotations[1]])
                plt.annotate("Frame Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x, y),
                             xytext=(-160, 30),
                             xycoords='data',
                             fontsize=15,
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

                (x, y, loss, fps) = (xs2[annotations[2]],
                                     ys2[annotations[2]],
                                     losses2[annotations[2]],
                                     fpses2[annotations[2]])
                plt.annotate("Frame Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x, y),
                             xytext=(-25, 50),
                             xycoords='data',
                             fontsize=15,
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

                (x, y, loss, fps) = (xs2[annotations[3]],
                                     ys2[annotations[3]],
                                     losses2[annotations[3]],
                                     fpses2[annotations[3]])
                plt.annotate("Frame Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x, y),
                             xytext=(-160, 30),
                             xycoords='data',
                             fontsize=15,
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

                (x, y, loss, fps) = (xs3[annotations[4]],
                                     ys3[annotations[4]],
                                     losses3[annotations[4]],
                                     fpses3[annotations[4]])
                plt.annotate("Frame Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x, y),
                             xytext=(-15, 25),
                             xycoords='data',
                             fontsize=15,
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

                (x, y, loss, fps) = (xs3[annotations[5]],
                                     ys3[annotations[5]],
                                     losses3[annotations[5]],
                                     fpses3[annotations[5]])
                plt.annotate("Frame Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x, y),
                             xytext=(-170, 70),
                             xycoords='data',
                             fontsize=15,
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

                plt.savefig(plot_dir + "/" + plot_file + "-f1-annotated.pdf")
            plt.clf()


root_dir = "output/streamer/scheduler/atc"


def main():
    # run_combinations()
    # run_fairness()
    run_combinations_left4pts()
    # run_x_voting()


def run_combinations():
    metric = "f1"
    ms0 = collect_comb_csvs("{root}/{metric}/combos/{metric}-combo-numapps-*-mainstream-simulator".format(root=root_dir, metric=metric))
    ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/combos/f1-4hybrid-combo-all-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-nosharing"
    f1 ="f1-4hybrid"
    t1 = ""
    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    titles = [t1]
    hybrid4_annotations = [1, 6, 1, 5, 3, 6]
    plot_dir = "plots/scheduler/atc/maximize-f1"
    plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, annotations = hybrid4_annotations, legend=True)
    plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, legend=True)


def run_combinations_left4pts():
    metric = "f1"
    ms1 = collect_comb_csvs("{root}/{metric}/combos/{metric}-4hybrid-combo-numapps-*-mainstream-simulator".format(root=root_dir, metric=metric))
    max1 = collect_comb_csvs("{root}/{metric}/combos/{metric}-4hybrid-combo-numapps-*-maxsharing".format(root=root_dir, metric=metric))
    min1 = collect_comb_csvs("{root}/{metric}/combos/{metric}-4hybrid-combo-numapps-*-nosharing".format(root=root_dir, metric=metric))
    f1 ="f1-4hybrid-combo"
    t1 = ""
    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    titles = [t1]
    plot_dir = "plots/scheduler/atc/maximize-f1"
    plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, xlim=(0, 5), legend=True)


def run_fairness():
    metric = "f1"
    ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-mainstream-simulator"
    ms_v1 =  "output/streamer/scheduler/atc/f1/f1-fairness-4hybrid-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-nosharing"
    f1 ="f1-fairness"
    t1 = "Mainstream with Fairness"
    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    titles = [t1]
    plot_dir = "plots/scheduler/atc/maximize-f1"
    plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, ms_variant_files=[ms_v1], ms_variant_name="Mainstream-Proportional-Fairness", legend=True)


def run_x_voting():
    for dataset in ["trains", "pedestrian"]:
        for metric in ["f1", "fnr", "fpr"]:
            ms0 = "output/streamer/scheduler/atc/{metric}/{metric}-{dataset}-500-mainstream-simulator".format(metric=metric, dataset=dataset)
            ms1 =  "output/streamer/scheduler/atc/{metric}/{metric}-{dataset}-500-x1-mainstream-simulator".format(metric=metric, dataset=dataset)
            ms2 =  "output/streamer/scheduler/atc/{metric}/{metric}-{dataset}-500-x2-mainstream-simulator".format(metric=metric, dataset=dataset)
            ms3 =  "output/streamer/scheduler/atc/{metric}/{metric}-{dataset}-500-x3-mainstream-simulator".format(metric=metric, dataset=dataset)
            l0 = "1-voting (for check)"
            l1 = "1-voting"
            l2 = "2-voting"
            l3 = "3-voting"
            f_name ="voting-{}-500-{}".format(dataset, metric)
            plot_dir = "plots/scheduler/"
            plot_x_voting([ms1, ms2, ms3, ms0], [l1, l2, l3, l0], f_name, plot_dir)


if __name__ == '__main__':
    main()
