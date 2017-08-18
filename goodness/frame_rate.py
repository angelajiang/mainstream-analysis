import pprint as pp
import sys
import matplotlib
import numpy as np

import matplotlib.pyplot as plt

from matplotlib.pyplot import cm

def get_data(csv_file):
    data_by_slo = {}
    xs = []
    ys = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            stride = int(vals[0])
            slo = int(vals[1])
            prob = float(vals[2])
            if slo not in data_by_slo.keys():
                data_by_slo[slo] = {"xs": [], "ys": []}
            data_by_slo[slo]["xs"].append(stride)
            data_by_slo[slo]["ys"].append(prob)
    return data_by_slo

def plot_models(rate_files, labels, plot_file, slo=None):
    # xs: stride
    # ys: probability
    # Each line is a model

    colors=cm.rainbow(np.linspace(0,1,len(labels)))

    for rate_file, label, color in zip(rate_files, labels, colors):
        data_by_slo = get_data(rate_file)
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
    plt.ylabel("Probability of detection", fontsize=25)
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

    data_by_slo = get_data(rate_file)
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
    plt.ylabel("Probability of detection", fontsize=25)
    plt.ylim(0,1)
    plt.legend(loc=0, fontsize=13)
    plt.tight_layout()

    plt.savefig(plot_file)
    plt.clf()

def tmp():
    fig = plt.figure()
    labels = ["Within .1 sec", "Within .5 sec", "Within 1 sec"]
    for l in labels:
        xs = range(1, 5)
        ys = [0] * 4
        plt.plot(xs, ys, label = l)
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.xlabel("Number of Apps", fontsize=25)
    plt.ylabel("P(detect all events)", fontsize=25)
    plt.legend(fontsize=20)
    plt.xticks(xs)
    plt.ylim(0,1)
    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    tmp()
    sys.exit()

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
    plot_models([f1, f3, f5, f7, f8, f9, f10, f11, f12, f13],
                ["7", "14", "41", "87", "133", "165", "197", "249", "280", "311"],
                plot_file,
                40)

    #plot_file = "plots/frame-rate/frame-rate-afn-slo.pdf"
    #plot_slos(f13, plot_file)
