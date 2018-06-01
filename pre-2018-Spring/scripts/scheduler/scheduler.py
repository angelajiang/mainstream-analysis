import os
import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from itertools import cycle
from scipy.stats import linregress
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

def plot_x_voting(ms_files, labels, plot_file, plot_dir, dual=False, frontier=False):
    colors = plot_util.COLORLISTS[4]
    colors = [colors[0], colors[3], colors[1], colors[2]]
    markers = plot_util.MARKERS[:len(ms_files)]

    metrics = ["f1", "recall", "precision"]
    titles = ["F1-score", "Recall", "Precision"]

    for metric, title in zip(metrics, titles):
        for i in range(2):
            fig, ax1 = plt.subplots()
            if dual:
                ax2 = ax1.twinx()

            lines = []
            all_pts = []
            for ms_file, label, c, m in zip(ms_files, labels, colors, markers):
                if metric == 'f1':
                    xs, ys, errs, losses, fpses = get_f1_data(ms_file)
                elif metric == 'recall':
                    xs, ys, errs, losses, fpses = get_recall_data(ms_file, 1)
                elif metric == 'precision':
                    xs, ys, errs, losses, fpses = get_precision_data(ms_file)
                if frontier:
                    if label == "7-voting":
                        lines.append(ax1.errorbar(xs, ys, yerr=errs, label=label, lw=2, markersize=6,
                                                  marker=m,
                                                  color=c))
                    else:
                        lines.append(ax1.errorbar(xs, ys, yerr=errs, label=label, lw=2, markersize=4,
                                                  marker=m,
                                                  color=c))
                    # lines.append(ax1.scatter(xs, ys, label=label, s=50,
                                             # edgecolor='black', marker=m, color=c))
                    all_pts += list(zip(xs, ys))
                else:
                    lines.append(ax1.errorbar(xs, ys, yerr=errs, label=label, lw=4, markersize=8,
                                              marker=m,
                                              color=c))
                if dual:
                    ax2.plot(xs, fpses, lw=2, markersize=8, alpha=0.2,
                             marker=m,
                             color=c)

            if frontier:
                if plot_file == 'voting-train-500-f1' and metric == 'f1':
                    xss, ys = plot_util.frontier(all_pts, True)
                else:
                    xss, ys = plot_util.frontier(all_pts, False)

                lines += ax1.plot(xss, ys, '--', label='Pareto Frontier', lw=7)

                ax1.set_ylim(0, 1)

            if dual:
                plot_util.format_plot_dual(ax1, ax2, "Number of concurrent apps", "Event " + title, "Average FPS")
            else:
                plot_util.format_plot("Number of concurrent apps", "Event " + title)
            ax1.set_xlim(max(min(xs),2), max(xs))

            filename = plot_dir + "/" + plot_file + "-" + metric
            if dual:
                filename += "-dual"
            if frontier:
                filename += "-frontier"
            labels = [l.get_label() for l in lines]
            leg = ax1.legend(lines, labels, loc=0, fontsize=15)
            leg.get_frame().set_alpha(0.5)
            plt.savefig(filename + ".pdf")


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

def plot_precision(ms_files, max_files, min_files, plot_files, titles, plot_dir, errbars=True):
    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):
            xs1, ys1, errs1, _, _ = get_precision_data(ms_file)
            xs2, ys2, errs2, _, _ = get_precision_data(max_file)
            xs3, ys3, errs3, _, _ = get_precision_data(min_file)

            if not errbars:
                errs3 = None
                errs2 = None
                errs1 = None
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

def plot_f1(ms_files, max_files, min_files, plot_files, titles, plot_dir, errbars=True,
                                                                          xlim=None,
                                                                          annotations = [],
                                                                          ms_variant_files=[],
                                                                          ms_variant_name=None,
                                                                          legend=True,
                                                                          legend_xargs={},
                                                                          normalize=False):
    # import matplotlib
    # matplotlib.use('ps')
    # matplotlib.rc('text', usetex=True)
    # matplotlib.rc('text.latex', preamble='\usepackage{xcolor}')
    for i in range(2):
        for i, (ms_file, max_file, min_file, plot_file, title) \
                in enumerate(zip(ms_files, max_files, min_files, plot_files, titles)):
            ms_variant_file = ms_variant_files[i] if ms_variant_files else None
            xs1, ys1, errs1, losses1, fpses1 = get_f1_data(ms_file)
            xs2, ys2, errs2, losses2, fpses2 = get_f1_data(max_file)
            xs3, ys3, errs3, losses3, fpses3 = get_f1_data(min_file)
            if ms_variant_file:
                xs4, ys4, errs4, losses4, fpses4 = get_f1_data(ms_variant_file)

            if xlim:
                plt.xlim(*xlim)
            else:
                plt.xlim(max(min(xs1),2), max(xs1))

            if not errbars:
                errs3 = None
                errs2 = None
                errs1 = None

            if normalize:
                ys2 = [y2 / float(y3) for y2, y3 in zip(ys2, ys3)]
                ys1 = [y1 / float(y3) for y1, y3 in zip(ys1, ys3)]
                plot_util.format_plot("Number of concurrent apps", "Benefit over NS")
            else:
                plt.ylim(0, 1)
                plot_util.format_plot("Number of concurrent apps", "Event F1-score")
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

            # To get calculation for atc2018.
            diffs = [[],[]]
            for x1, y1, x2, y2, x3, y3 in zip(xs1, ys1, xs2, ys2, xs3, ys3):
                # print "should be same", x1, x2, x3
                assert x1 == x2 == x3
                print x1, y1, y2, y3, "%", y1/y2, y1/y3
                diffs[0].append(y1/y2)
                diffs[1].append(y1/y3)
                # print "difference", 0., y1 - y2, y1 - y3
            print "max", max(diffs[0]), max(diffs[1])

            if ms_variant_file:
                plt.errorbar(xs4, ys4, yerr=errs4, lw=4, markersize=8,
                             marker=plot_util.MAINSTREAM_VARIANT['marker'],
                             color=plot_util.MAINSTREAM_VARIANT['color'],
                             label=ms_variant_name if ms_variant_name else plot_util.MAINSTREAM_VARIANT['label'])

            if legend:
                leg = plt.legend(**legend_xargs)
                leg.get_frame().set_alpha(0.5)

            plt.savefig(plot_dir + "/" + plot_file + "-f1.pdf")

            if len(annotations) > 0:
                assert len(annotations) == 6

                annotations_params = [
                    {'xy': (-30, 30), 'src': 1, 'name': 'a'},
                    {'xy': (-280, 40), 'src': 1, 'name': 'b'},
                    {'xy': (15, -70), 'src': 2, 'name': 'e'},
                    {'xy': (-130, -40), 'src': 2, 'name': 'd'},
                    {'xy': (35, -25), 'src': 3, 'name': 'c'},
                    {'xy': (-170, 30), 'src': 3, 'name': 'f'},
                ]
                for annotation, params in zip(annotations, annotations_params):
                    if params['src'] == 1:
                        (x, y, loss, fps) = (xs1[annotation],
                                             ys1[annotation],
                                             losses1[annotation],
                                             fpses1[annotation])
                    elif params['src'] == 2:
                        (x, y, loss, fps) = (xs2[annotation],
                                             ys2[annotation],
                                             losses2[annotation],
                                             fpses2[annotation])
                    elif params['src'] == 3:
                        (x, y, loss, fps) = (xs3[annotation],
                                             ys3[annotation],
                                             losses3[annotation],
                                             fpses3[annotation])

                    # plt.annotate("\\textcolor{{red}}{{({})}} Frame Acc: {}, FPS: {}".format(params["name"], 1-loss, fps),                         fpses3[annotation])
                    plt.annotate("({}) Frame Acc: {}, FPS: {}".format(params["name"], 1-loss, fps),
                                 xy=(x, y),
                                 xytext=params['xy'],
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
    # run_combinations_left4pts()
    run_x_voting()


def run_combinations():
    metric = "f1"
    ms0 = collect_comb_csvs("{root}/{metric}/combos/{metric}-combo-numapps-*-mainstream-simulator".format(root=root_dir, metric=metric))
    ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/combos/f1-4hybrid-combo-all-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-nosharing"
    f1 = "f1-4hybrid-combos"
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
    plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, xlim=(1, 4), legend=True, legend_xargs=dict(loc=0))


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
    max_x = 7
    selected_x = [1, 3, 5, 7]
    for dataset in ["train", "pedestrian"]:
        for metric in ["f1"]: #, "fnr", "fpr"]:
            # ms0 = "output/streamer/scheduler/atc/{metric}/{metric}-{dataset}-500-mainstream-simulator".format(metric=metric, dataset=dataset)
            # l0 = "1-voting (for check)"
            mses = ["output/streamer/scheduler/atc/{metric}/{metric}-{dataset}-500-x{x}-mainstream-simulator".format(metric=metric, dataset=dataset, x=i) for i in selected_x]
            lines = ["{}-voting".format(i) for i in selected_x]
            f_name ="voting-{}-500-{}".format(dataset, metric)
            plot_dir = "plots/scheduler/"
            # plot_x_voting(mses, lines, f_name, plot_dir)
            plot_x_voting(mses, lines, f_name, plot_dir, frontier=True)
            plot_x_voting(mses, lines, f_name, plot_dir, dual=True)


if __name__ == '__main__':
    main()
