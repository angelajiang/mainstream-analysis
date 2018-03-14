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
from data_util_fair import load_dfs, filter_dfs

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()


sizes = {
    'label': 26,
    'legend': 20,
    'title': 35,
}


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
    agg = ['Max', 'Avg']
    labels = ['Worst', 'Average']
    lss = ['o-', 'X--']
    colors = [plot_util.COLORS["red"], plot_util.COLORS["blue"]]
    for x, label, ls, color in zip(agg, labels, lss, colors):
        data = grp[x + ' FNR Loss'].mean()
        # errs = grp[x + ' FNR Loss'].std()
        xs, ys = data.index, data.values
        # plt.plot(xs, ys, ls, label=x + ' FNR Loss amongst applications')
        # plt.errorbar(xs, ys, yerr=errs, lw=2,
        #              # linestyle=ls,
        #              marker='o',
        #              color=color,
        #              label=label + ' FNR Loss amongst concurrent apps')
        plt.plot(xs, ys, lw=2, marker='o', color=color, label=label + ' FNR Loss\namongst concurrent apps')

    plt.legend(loc=0, fontsize=sizes['legend'])

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.title(title, fontsize=sizes['title'])
    plt.xlabel("Number of concurrent apps", fontsize=sizes['label'])
    plt.xlim(2, max(xs))
    plt.ylim(0, None)
    plt.ylabel("False negative rate loss", fontsize=sizes['label'])
    plt.tight_layout()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)
    plt.savefig(plot_dir + "/" + plot_file + ".pdf")
    plt.clf()


if __name__ == "__main__":

    # prefix = "../mainstream/log"
    #prefix = "output/streamer/scheduler/combinations"
    prefix = "../data"

    f1 = "scheduler-apps-fairness"
    t1 = ""
    plot_dir = "plots/scheduler"

    f_files = [f1]
    titles = [t1]

    plot(prefix, f_files, titles, plot_dir)
