import matplotlib
import sys
sys.path.append("scripts")
import scheduler

sys.path.append("scripts/util")
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def plot_f1_dual(*args, **kwargs):
    plot_dual("f1", "F1-score", *args, **kwargs)

def plot_recall_dual(*args, **kwargs):
    plot_dual("recall", "Recall", *args, **kwargs)

def plot_precision_dual(*args, **kwargs):
    plot_dual("precision", "Precision", *args, **kwargs)

def plot_dual(metric, metric_title, ms_files, max_files, min_files, plot_files, titles, plot_dir, annotated=False):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    if metric == "f1":
        get_data = scheduler.get_f1_data
    elif metric == "recall":
        get_data = lambda x: scheduler.get_recall_data(x, 1)
    elif metric == "precision":
        get_data = scheduler.get_precision_data

    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):

            data = []

            data.append(get_data(min_file))
            data.append(get_data(max_file))
            data.append(get_data(ms_file))
            utils = [plot_util.NO_SHARING, plot_util.MAX_SHARING, plot_util.MAINSTREAM]

            ax2_params = dict(lw=3, markersize=8, alpha=0.7, linestyle='--')
            ax2_lines = []

            for row, util in zip(data, utils):
                xs, ys, errs, losses, fpses = row
                ax2_lines += ax2.plot(xs, fpses,
                                      marker=util['marker_alt'],
                                      color=util['color'],
                                      label=util['label'],
                                      **ax2_params)
            ax1_lines = []
            for row, util in zip(data, utils):
                xs, ys, errs, losses, fpses = row
                ax1_lines += ax1.plot(xs, ys, lw=4, markersize=8,
                                      marker=util['marker'],
                                      color=util['color'],
                                      label=util['label'])

            plot_util.format_plot_dual(ax1, ax2, "Number of concurrent apps", "Event " + metric_title, "Average FPS")
            ax1.set_xlim(max(min(xs),2), max(xs))
            lns = ax1_lines
            labels = [l.get_label() + ' (FPS, {})'.format(metric_title) for l in lns]
            if metric == "f1":
                leg = ax1.legend(lns, labels, loc=4, bbox_to_anchor=[1.01, .1], fontsize=13, borderpad=None)
                leg.get_frame().set_linewidth(0.0)
                leg2 = ax2.legend(ax2_lines, [""] * len(lns), loc=4, bbox_to_anchor=[.5, .1], fontsize=13, borderpad=None, frameon=False)
                leg2.get_frame().set_linewidth(0.0)

            plt.savefig(plot_dir + "/" + plot_file + "-" + metric + "-dual.pdf")

if __name__ == "__main__":

    ################ F1-score ##################

    plot_dir = "plots/scheduler/atc/maximize-f1"
    t1 = ""

    ms1 =  "output/streamer/scheduler/atc/f1/f1-pedestrian-500-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-pedestrian-500-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-pedestrian-500-nosharing"
    f1 ="f1-pedestrian-500"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    plot_recall_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)

    ms1 =  "output/streamer/scheduler/atc/f1/f1-train-500-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-train-500-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-train-500-nosharing"
    f1 ="f1-train-500"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    plot_recall_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    plot_precision_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
