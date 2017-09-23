import pprint as pp
import sys
import matplotlib
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

import seaborn as sns

sns.set_style("whitegrid")

def plot_fpf_by_stride(avg_fpf, ns_fpf, ms_fpf, plot_file):
    # strides: strides
    # xs: sample rate
    # ys: false positive frequency

    num_frames = 1787
    xs = [x * 0.1 for x in range(0, 11)]
    ys = []

    for rate in xs:
        fpf = avg_fpf * rate
        ys.append(fpf)

    ns_intercept = ns_fpf / avg_fpf
    ms_intercept = ms_fpf / avg_fpf

    plt.axhline(y= ns_fpf, linestyle="--", color="black", alpha=0.4, linewidth=2)
    plt.axhline(y= ms_fpf, linestyle="--", color="black", alpha=0.4, linewidth=2)

    plt.plot(xs, ys, linewidth=2)

    plt.annotate("False positive rate", 
                 xy=(xs[-1], ys[-1]),
                 xytext=(-250, -20),
                 xycoords='data',
                 fontsize=21,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    plt.annotate("No Sharing FPF", 
                 xy=(ns_intercept, ns_fpf),
                 xytext=(100, 20),
                 xycoords='data',
                 fontsize=21,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    plt.annotate("Mainstream FPF", 
                 xy=(ms_intercept, ms_fpf),
                 xytext=(-200, 20),
                 xycoords='data',
                 fontsize=21,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.xlabel("Sample rate", fontsize=35)
    plt.ylabel("False Positive Freq", fontsize=35)
    plt.xlim(0,1)
    plt.gca().xaxis.grid(True)
    plt.legend(loc=0, fontsize=20)
    plt.tight_layout()

    plt.savefig(plot_file + "-fpf-by-stride.pdf")
    plt.clf()

if __name__ == "__main__":
    plot_file = "plots/goodness/vid4"
    plot_fpf_by_stride(0.028,  0.0011, 0.015, plot_file)


