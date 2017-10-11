import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from itertools import cycle
from scipy.stats import linregress, hmean

sys.path.append("scripts/util")
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()


def get_fnr_data(csv_file, version):
    # Version 0: num_apps,fnr,acc_loss,fps_list...,frozen_list...
    # Version 1: num_apps,fnr,fpr,acc_loss,fps_list...,frozen_list...
    metrics = {}
    fpses = {}
    acc_losses = {}
    xs = []
    ys = []
    errs = []
    as1 = []
    as2 = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            if version == 0:
                acc_loss = round(float(vals[2]),2)
                fps_start = num_apps + 4
                fps_end = (2 *num_apps) + 3
                fps_list = [float(v) for v in vals[fps_start:fps_end]]
                average_fps = round(np.average(fps_list),2)
            if version == 1:
                acc_loss = round(float(vals[3]),2)
                fps_start = num_apps + 5
                fps_end = (2 *num_apps) + 4
                fps_list = [float(v) for v in vals[fps_start:fps_end]]
                average_fps = round(np.average(fps_list), 2)

            if num_apps not in metrics.keys():
                xs.append(num_apps)
                metrics[num_apps] = []
                acc_losses[num_apps] = []
                fpses[num_apps] = []

            fnr = float(vals[1])
            metrics[num_apps].append(fnr)
            acc_losses[num_apps].append(acc_loss)
            fpses[num_apps].append(average_fps)

    for x in xs:
        ys.append(np.average(metrics[x]))
        errs.append(np.std(metrics[x]))
        as1.append(round(np.average(acc_losses[x]), 2))
        as2.append(round(np.average(fpses[x]), 2))
    return xs, ys, errs, as1, as2

def get_fpr_data(csv_file):
    # Assumes Version 1
    # Version 1: num_apps,fnr,fpr,acc_loss,fps_list...,frozen_list...
    metrics = {}
    xs = []
    ys = []
    errs = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])

            if num_apps not in metrics.keys():
                xs.append(num_apps)
                metrics[num_apps] = []

            fnr = float(vals[1])
            fpr = float(vals[2])
            metrics[num_apps].append(fpr)

    for x in xs:
        ys.append(np.average(metrics[x]))
        errs.append(np.std(metrics[x]))
    return xs, ys, errs


def get_f1_data(csv_file):
    # Assumes Version 1
    # Version 1: num_apps,fnr,fpr,acc_loss,fps_list...,frozen_list...
    metrics = {}
    xs = []
    ys = []
    errs = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])

            if num_apps not in metrics.keys():
                xs.append(num_apps)
                metrics[num_apps] = []

            fnr = float(vals[1])
            fpr = float(vals[2])
            f1 = hmean([1 - float(fnr), 1 - float(fpr)])
            metrics[num_apps].append(f1)

    for x in xs:
        ys.append(np.average(metrics[x]))
        errs.append(np.std(metrics[x]))
    return xs, ys, errs


def plot_fnr(ms_files, max_files, min_files, plot_files, titles, plot_dir, annotated=False, version=0):
    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):
            xs1, ys1, errs1, losses1, fpses1 = get_fnr_data(ms_file, version)
            xs2, ys2, errs2, losses2, fpses2 = get_fnr_data(max_file, version)
            xs3, ys3, errs3, losses3, fpses3 = get_fnr_data(min_file, version)

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

            if annotated:
                for x1, y1, loss, fps in zip(xs1[0::5], ys1[0::5], losses1[0::5], fpses1[0::5]):
                    plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                                 xy=(x1, y1),
                                 xytext=(25, 50),
                                 xycoords='data',
                                 fontsize=15,
                                 textcoords='offset points',
                                 arrowprops=dict(arrowstyle="->"))

                for x2, y2, loss, fps in zip(xs2[2::4], ys2[2::4], losses2[2::4], fpses2[2::4]):
                    plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                                 xy=(x2, y2),
                                 xytext=(-25, -50),
                                 xycoords='data',
                                 fontsize=15,
                                 textcoords='offset points',
                                 arrowprops=dict(arrowstyle="->"))

                for x3, y3, loss, fps in zip(xs3[2::4], ys3[2::4], losses3[2::4], fpses3[2::4]):
                    plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                                 xy=(x3, y3),
                                 xytext=(-15, -25),
                                 xycoords='data',
                                 fontsize=15,
                                 textcoords='offset points',
                                 arrowprops=dict(arrowstyle="->"))

            plt.legend(loc=0, fontsize=15)

            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.tick_params(axis='x', which='major', labelsize=28)
            plt.tick_params(axis='x', which='minor', labelsize=20)

            #plt.title(title, fontsize=35)
            plt.xlabel("Number of concurrent apps", fontsize=30)
            plt.xlim(2, max(xs1))
            plt.ylim(0, 1)
            plt.ylabel("False negative rate", fontsize=30)
            plt.tight_layout()
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)
            plt.savefig(plot_dir + "/" + plot_file + "-fnr.pdf")
            plt.clf()

def plot_fpr(ms_files, max_files, min_files, plot_files, titles, plot_dir):
    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):
            xs1, ys1, errs1 = get_fpr_data(ms_file)
            xs2, ys2, errs2 = get_fpr_data(max_file)
            xs3, ys3, errs3 = get_fpr_data(min_file)

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

            plt.legend(loc=0, fontsize=15)

            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.tick_params(axis='x', which='major', labelsize=28)
            plt.tick_params(axis='x', which='minor', labelsize=20)

            #plt.title(title, fontsize=35)
            plt.xlabel("Number of concurrent apps", fontsize=30)
            plt.xlim(2, max(xs1))
            plt.ylim(0, 1)
            plt.ylabel("False Positive Rate", fontsize=30)
            plt.tight_layout()
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)
            plt.savefig(plot_dir + "/" + plot_file + "-fpr.pdf")
            plt.clf()

def plot_f1(ms_files, max_files, min_files, plot_files, titles, plot_dir):
    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):
            xs1, ys1, errs1 = get_f1_data(ms_file)
            xs2, ys2, errs2 = get_f1_data(max_file)
            xs3, ys3, errs3 = get_f1_data(min_file)

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

            plt.legend(loc=0, fontsize=15)

            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.tick_params(axis='x', which='major', labelsize=28)
            plt.tick_params(axis='x', which='minor', labelsize=20)

            #plt.title(title, fontsize=35)
            plt.xlabel("Number of concurrent apps", fontsize=30)
            plt.xlim(2, max(xs1))
            plt.ylim(0, 1)
            plt.ylabel("F1 Score", fontsize=30)
            plt.tight_layout()
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)
            plt.savefig(plot_dir + "/" + plot_file + "-f1.pdf")
            plt.clf()

if __name__ == "__main__":

    ms1 = "output/streamer/scheduler/correlation/scheduler-correlation-mainstream-c0.1664-ll0" 
    max1 = "output/streamer/scheduler/correlation/scheduler-correlation-maxsharing-c0.1664" 
    min1 = "output/streamer/scheduler/correlation/scheduler-correlation-nosharing-c0.1664" 
    f1 ="scheduler-false-neg-rate"
    t1 = ""
    plot_dir = "plots/scheduler"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ms1 = "output/streamer/scheduler/v1/scheduler-v1-500-c0.1664-mainstream"
    max1 = "output/streamer/scheduler/v1/scheduler-v1-500-c0.1664-maxsharing"
    min1 = "output/streamer/scheduler/v1/scheduler-v1-500-c0.1664-nosharing"
    f1 ="scheduler-500-c0.1664-ll2"
    t1 = ""
    plot_dir = "plots/scheduler/v1/"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    plot_fpr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
