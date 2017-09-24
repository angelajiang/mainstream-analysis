import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from itertools import cycle
from scipy.stats import linregress

sys.path.append("scripts/util")
import plot_util
sys.path.append("notebooks")
from data_util import load_dfs, filter_dfs

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()


def load_data(prefix):
    df_all, baselines_fnr = load_dfs(prefix)

    # Filter DFs
    # select_dfs = [2, 3, 4, 6]
    select_dfs = [2, 3, 4]
    df_all = filter_dfs(df_all, select_dfs)
    return df_all, baselines_fnr


def plot(prefix, f_files, titles, plot_dir, annotated=False):
    df_all, baselines_fnr = load_data(prefix)

    title = titles[0]
    plot_file = f_files[0]


    # sns.set_style('ticks')
    grp = df_all.groupby('No of applications')
    lss = ['o-', 'X--']
    colors = [plot_util.COLORS["red"], plot_util.COLORS["blue"]]
    for x, ls, color in zip(['Max', 'Avg'], lss, colors):
        data = grp[x + ' FNR Loss'].mean()
        errs = grp[x + ' FNR Loss'].std()
        xs, ys = data.index, data.values
        # plt.plot(xs, ys, ls, label=x + ' FNR Loss amongst applications')
        plt.errorbar(xs, ys, yerr=errs, lw=2,
                     # linestyle=ls,
                     marker='o',
                     color=color,
                     label=x.replace('Avg', 'Average') + ' FNR Loss amongst applications')

        # xs1, ys1, errs1, losses1, fpses1 = get_data(ms_file)
        # xs2, ys2, errs2, losses2, fpses2 = get_data(max_file)
        # xs3, ys3, errs3, losses3, fpses3 = get_data(min_file)

        # plt.errorbar(xs3, ys3, yerr=errs3, lw=2,
        #              marker=plot_util.NO_SHARING['marker'],
        #              color=plot_util.NO_SHARING['color'],
        #              label=plot_util.NO_SHARING['label'])
        # plt.errorbar(xs2, ys2, yerr=errs2, lw=2,
        #              marker=plot_util.MAX_SHARING['marker'],
        #              color=plot_util.MAX_SHARING['color'],
        #              label=plot_util.MAX_SHARING['label'])
        # plt.errorbar(xs1, ys1, yerr=errs1, lw=2,
        #              marker=plot_util.MAINSTREAM['marker'],
        #              color=plot_util.MAINSTREAM['color'],
        #              label=plot_util.MAINSTREAM['label'])

        # if annotated:
        #     for x1, y1, loss, fps in zip(xs1[0::5], ys1[0::5], losses1[0::5], fpses1[0::5]):
        #         plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
        #                      xy=(x1, y1),
        #                      xytext=(25, 50),
        #                      xycoords='data',
        #                      fontsize=15,
        #                      textcoords='offset points',
        #                      arrowprops=dict(arrowstyle="->"))

        #     for x2, y2, loss, fps in zip(xs2[2::4], ys2[2::4], losses2[2::4], fpses2[2::4]):
        #         plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
        #                      xy=(x2, y2),
        #                      xytext=(-25, -50),
        #                      xycoords='data',
        #                      fontsize=15,
        #                      textcoords='offset points',
        #                      arrowprops=dict(arrowstyle="->"))

        #     for x3, y3, loss, fps in zip(xs3[2::4], ys3[2::4], losses3[2::4], fpses3[2::4]):
        #         plt.annotate("Acc:" + str(1-loss) + ", FPS:" + str(fps), 
        #                      xy=(x3, y3),
        #                      xytext=(-15, -25),
        #                      xycoords='data',
        #                      fontsize=15,
        #                      textcoords='offset points',
        #                      arrowprops=dict(arrowstyle="->"))

    plt.legend(loc=0, fontsize=15)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.title(title, fontsize=35)
    plt.xlabel("Number of concurrent apps", fontsize=30)
    plt.xlim(2, max(xs))
    plt.ylim(0, None)
    plt.ylabel("False negative rate loss", fontsize=30)
    plt.tight_layout()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)
    plt.savefig(plot_dir + "/" + plot_file + ".pdf")
    plt.clf()


if __name__ == "__main__":

    # prefix = "../mainstream/log"
    prefix = "output/streamer/scheduler/combinations"

    f1 = "scheduler-apps-fairness"
    t1 = ""
    plot_dir = "plots/scheduler"

    f_files = [f1]
    titles = [t1]

    plot(prefix, f_files, titles, plot_dir)

