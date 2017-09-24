import pprint as pp
import sys
import matplotlib
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.pyplot import cm

import seaborn as sns

sns.set_style("whitegrid")

def plot_fpf_by_stride(stream_fps, avg_fpf, ns_fpf, ms_fpf, msv_fpf, ns_fps, ms_fps, plot_file):
    # strides: strides
    # xs: sample rate
    # ys: false positive frequency

    num_frames = 1787
    xs = [x * 0.1 for x in range(0, 11)]
    ys = []

    for rate in xs:
        fpf = avg_fpf * rate
        ys.append(fpf)

    ns_sample_rate = float(ns_fps) / stream_fps
    ms_sample_rate = float(ms_fps) / stream_fps
    msv_sample_rate = float(ms_fps) / stream_fps

    plt.plot(xs, ys, linewidth=2)

    plt.plot([xs[-1]], [ys[-1]], marker='o', markersize=7, color="red")
    plt.plot([ns_sample_rate], [ns_fpf], marker='o', markersize=7, color="blue")
    plt.plot([ns_sample_rate], [ns_fpf], marker='o', markersize=7, color="green")
    plt.plot([ms_sample_rate], [ms_fpf], marker='*', markersize=10, color="black")
    plt.plot([msv_sample_rate], [msv_fpf], marker='*', markersize=10, color="magenta")

    plt.annotate("False positive rate", 
                 xy=(xs[-1], ys[-1]),
                 xytext=(-250, -20),
                 xycoords='data',
                 fontsize=21,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    plt.annotate("NS FPF", 
                 xy=(ns_sample_rate, ns_fpf),
                 xytext=(0, 70),
                 xycoords='data',
                 fontsize=21,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    plt.annotate("MS FPF", 
                 xy=(ms_sample_rate, ms_fpf),
                 xytext=(-20, 30),
                 xycoords='data',
                 fontsize=21,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    plt.annotate("MS 2-voting FPF", 
                 xy=(msv_sample_rate, msv_fpf),
                 xytext=(0, 50),
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
    plot_fpf_by_stride(15, 0.028,  0.0011, 0.015, 0.00056, 1.3, 7, plot_file)

