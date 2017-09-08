import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from itertools import cycle
from scipy.stats import linregress


matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def get_data(csv_file):
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
            acc_loss = round(float(vals[2]),2)
            fps_list = [float(v) for v in vals[(4+num_apps):]]
            average_fps = round(np.average(fps_list),2)

            if num_apps not in metrics.keys():
                xs.append(num_apps)
                metrics[num_apps] = []
                acc_losses[num_apps] = []
                fpses[num_apps] = []
            metric = float(vals[1])
            metrics[num_apps].append(metric)
            acc_losses[num_apps].append(acc_loss)
            fpses[num_apps].append(average_fps)

    for x in xs:
        ys.append(np.average(metrics[x]))
        errs.append(np.std(metrics[x]))
        as1.append(round(np.average(acc_losses[x]), 2))
        as2.append(round(np.average(fpses[x]), 2))
    return xs, ys, errs, as1, as2

def plot(ms_files, max_files, min_files, plot_files, titles, plot_dir):
    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):
            xs1, ys1, errs1, losses1, fpses1 = get_data(ms_file)
            xs2, ys2, errs2, losses2, fpses2 = get_data(max_file)
            xs3, ys3, errs3, losses3, fpses3 = get_data(min_file)

            plt.errorbar(xs1, ys1, yerr=errs1, marker="o", lw=2, label="Mainstream")
            plt.errorbar(xs2, ys2, yerr=errs2, marker="h", lw=2, label="Max sharing")
            plt.errorbar(xs3, ys3, yerr=errs3, marker="D", lw=2, label="No sharing")

            for x1, y1, loss, fps in zip(xs1[0::4], ys1[0::4], losses1[0::4], fpses1[0::4]):
                plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x1, y1),
                             xytext=(-70, 25),
                             xycoords='data',
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

            for x2, y2, loss, fps in zip(xs2[2::4], ys2[2::4], losses2[2::4], fpses2[2::4]):
                plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x2, y2),
                             xytext=(-15, 25),
                             xycoords='data',
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

            for x3, y3, loss, fps in zip(xs3[3::4], ys3[3::4], losses3[3::4], fpses3[3::4]):
                plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
                             xy=(x3, y3),
                             xytext=(10, -25),
                             xycoords='data',
                             textcoords='offset points',
                             arrowprops=dict(arrowstyle="->"))

            plt.legend(loc=0)

            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.tick_params(axis='x', which='major', labelsize=28)
            plt.tick_params(axis='x', which='minor', labelsize=20)

            plt.title(title, fontsize=28)
            plt.xlabel("Number of apps", fontsize=28)
            plt.xlim(2, max(xs1))
            plt.ylim(0, 1)
            plt.ylabel("False negative rate", fontsize=28)
            plt.tight_layout()
            plt.grid()
            plt.show()
            plt.savefig(plot_dir + "/" + plot_file + ".pdf")
            plt.clf()

if __name__ == "__main__":
    plot_dir = "plots/scheduler"

    ms1 = "output/streamer/scheduler/scheduler-s0-100-ms.csv" 
    max1 = "output/streamer/scheduler/scheduler-s0-100-max.csv" 
    min1 = "output/streamer/scheduler/scheduler-s0-100-min.csv" 
    f1 ="scheduler-s0-100"
    t1 = "Within 100ms (1.4 Frames)"

    ms2 = "output/streamer/scheduler/scheduler-s0-500-ms.csv" 
    max2 = "output/streamer/scheduler/scheduler-s0-500-max.csv" 
    min2 = "output/streamer/scheduler/scheduler-s0-500-min.csv" 
    f2 ="scheduler-s0-500"
    t2 = "Within 500ms (7 Frames)"

    ms3 = "output/streamer/scheduler/scheduler-s0-app10-ms.csv" 
    max3 = "output/streamer/scheduler/scheduler-s0-app10-max.csv" 
    min3 = "output/streamer/scheduler/scheduler-s0-app10-min.csv" 
    f3 ="scheduler-s0-250"
    t3 = "Within 250ms (2.8 Frames)"

    ms_files = [ms1, ms2, ms3]
    max_files = [max1, max2, max3]
    min_files = [min1, min2, min3]
    f_files = [f1, f2, f3]
    titles = [t1, t2, t3]

    plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
