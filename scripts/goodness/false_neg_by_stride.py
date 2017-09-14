import pprint as pp
import sys
import matplotlib
import numpy as np

import matplotlib.pyplot as plt

from matplotlib.pyplot import cm

def get_data_by_stride_and_slo(csv_file):
    data_by_slo = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            stride = int(vals[0])
            slo = int(vals[1])
            prob = 1 - float(vals[2])
            if slo not in data_by_slo.keys():
                data_by_slo[slo] = {"xs": [], "ys": []}
            data_by_slo[slo]["xs"].append(stride)
            data_by_slo[slo]["ys"].append(prob)
    return data_by_slo

def get_data(csv_file):
    data = {"strides": [], "ys": []}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            stride = int(vals[0])
            prob = 1 - float(vals[1])
            data["strides"].append(stride)
            data["ys"].append(prob)
    return data

def plot_models(rate_files, labels, plot_file, slo=None):
    # xs: stride
    # ys: probability
    # Each line is a model

    colors=cm.rainbow(np.linspace(0,1,len(labels)))

    for rate_file, label, color in zip(rate_files, labels, colors):
        data_by_slo = get_data_by_stride_and_slo(rate_file)
        if slo == None:
            slo = max(data_by_slo.keys())
        if slo not in data_by_slo.keys():
            print slo, "not in data_by_slo"
            sys.exit()
        xs = data_by_slo[slo]["xs"]
        ys = data_by_slo[slo]["ys"]
        plt.plot(xs, ys, label=label+" frozen", lw=2, color=color)

    plt.title("Detection within " + str(slo) + " frames")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.xlabel("Stride", fontsize=25)
    plt.ylabel("False negative rate", fontsize=25)
    plt.xlim(0, 100)
    plt.ylim(0, 1)
    plt.legend(loc=0, fontsize=15)
    plt.tight_layout()

    plt.savefig(plot_file)
    plt.clf()

def plot_slos(rate_file, plot_file):
    # xs: stride
    # ys: probability
    # Each line is a SLO

    fps = 1

    data_by_slo = get_data_by_stride_and_slo(rate_file)
    colors=cm.rainbow(np.linspace(0,1,len(data_by_slo.keys())))

    slos = sorted(data_by_slo.keys())
    for slo in slos:
        data = data_by_slo[slo]
        xs = data["xs"]
        ys = data["ys"]
        label = "W/in " + str(slo) + " frames (" + str(round(float(slo)/fps,2)) +" sec)"
        plt.plot(xs, ys, label=label, lw=2)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.xlabel("Stride", fontsize=25)
    plt.ylabel("False negative rate", fontsize=25)
    plt.xlim(0, 30)
    plt.ylim(0,1)
    plt.legend(loc=0, fontsize=13)
    plt.tight_layout()

    plt.savefig(plot_file)
    plt.clf()

def plot_dependence(files, labels, event_lengths, plot_file):
    # strides: strides
    # xs: sample rate
    # ys: probability

    fps = 1

    for filename, label in zip(files, labels):

        data = get_data(filename)
        strides = sorted(data.keys())

        strides = data["strides"]
        xs = [1 / float(s) for s in strides]
        xlabels = ["1/" + str(s) for s in strides]
        ys = data["ys"]
        plt.plot(xs, ys, label=label, lw=2)

    max_y = 0.4

    for length in event_lengths:
        plt.axvline(x= 1.0 / length, linestyle="--", color="black", alpha=0.3)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.xlabel("Sample rate", fontsize=28)
    plt.ylabel("False negative rate", fontsize=28)
    plt.xticks(xs, xlabels)
    plt.xscale('log')
    plt.xlim(0,1)
    plt.ylim(0, max_y)
    plt.legend(loc=0, fontsize=20)
    plt.tight_layout()

    plt.savefig(plot_file)
    plt.clf()

if __name__ == "__main__":

    f1 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/7"
    f2 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/10"
    f3 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/14"
    f4 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/18"
    f5 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/41"
    f6 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/64"
    f7 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/87"
    f8 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/133"
    f9 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/165"
    f10 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/197"
    f11 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/249"
    f12 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/280"
    f13 = "/Users/angela/src/private/mainstream/log/frame-rate/flowers/synthetic/311"
    plot_file = "plots/frame-rate/frame-rate-flowers-models.pdf"
    '''
    plot_models([f1, f3, f5, f7, f8, f9, f10, f11, f12, f13],
                ["7", "14", "41", "87", "133", "165", "197", "249", "280", "311"],
                plot_file,
                40)
    '''

    f1 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-0"
    f2 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-4"
    f3 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-17"
    f4 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-18"
    f5 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-41"
    f6 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-87"
    f7 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-165"
    f8 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-197"
    f9 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-229"
    f10 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-249"
    f11 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-280"
    f12 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-311"
    f13 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-313"
    plot_file = "plots/frame-rate/frame-rate-afn-models.pdf"
   # plot_models([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13],
   #      ["0", "4", "17", "18", "41", "87", "165", "197", "229", "249", "280", "311", "313"], plot_file)

    plot_file = "plots/frame-rate/frame-rate-afn-slo.pdf"
    #plot_slos(f13, plot_file)

    event_lengths = [286, 77, 92, 437, 274, 255, 251, 153]

    plot_file = "plots/frame-rate/frame-rate-afn-dependences.pdf"
    dependent_file = "/Users/angela/src/private/mainstream-analysis/output/mainstream/frame-rate/no-afn/train/v2/trains-313-dependent-whole"
    independent_file = "/Users/angela/src/private/mainstream-analysis/output/mainstream/frame-rate/no-afn/train/v2/trains-313-independent-whole"
    empirical_file = "/Users/angela/src/private/mainstream-analysis/output/mainstream/frame-rate/no-afn/train/v2/trains-313-empirical-temporal"
    files = [dependent_file, independent_file, empirical_file]
    labels = ["Dependent", "Independent", "Empirical"]
    plot_dependence(files, labels, event_lengths, plot_file)

    plot_file = "plots/frame-rate/frame-rate-afn-dependences2.pdf"
    dependent_file = "/Users/angela/src/private/mainstream-analysis/output/mainstream/frame-rate/no-afn/train/v2/trains-313-dependent"
    independent_file = "/Users/angela/src/private/mainstream-analysis/output/mainstream/frame-rate/no-afn/train/v2/trains-313-independent"
    empirical_file = "/Users/angela/src/private/mainstream-analysis/output/mainstream/frame-rate/no-afn/train/v2/trains-313-empirical-temporal"
    files = [dependent_file, independent_file, empirical_file]
    labels = ["Dependent", "Independent", "Empirical"]
    plot_dependence(files, labels, event_lengths, plot_file)

