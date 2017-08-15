import pprint as pp
import sys
import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

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

def plot_models(rate_files, labels, plot_file):
    # xs: stride
    # ys: probability
    # Each line is a model

    colors=cm.rainbow(np.linspace(0,1,len(labels)))

    for rate_file, label, color in zip(rate_files, labels, colors):
        data_by_slo = get_data(rate_file)
        max_slo = max(data_by_slo.keys())
        xs = data_by_slo[max_slo]["xs"]
        ys = data_by_slo[max_slo]["ys"]
        plt.plot(xs, ys, label=label+" frozen", lw=2, color=color)

    plt.title("Detection within " + str(max_slo) + " frames")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.xlabel("Stride", fontsize=25)
    plt.ylabel("Probability of detection", fontsize=25)
    plt.legend(loc=4, fontsize=15)
    plt.tight_layout()

    plt.savefig(plot_file)
    plt.clf()

def plot_slos(rate_file, plot_file):
    # xs: stride
    # ys: probability
    # Each line is a SLO

    data_by_slo = get_data(rate_file)
    colors=cm.rainbow(np.linspace(0,1,len(data_by_slo.keys())))

    slos = sorted(data_by_slo.keys())
    for slo in slos:
        data = data_by_slo[slo]
        xs = data["xs"]
        ys = data["ys"]
        plt.plot(xs, ys, label="Within " + str(slo) + " frames", lw=2)

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.xlabel("Stride", fontsize=25)
    plt.ylabel("Probability of detection", fontsize=25)
    plt.legend(loc=4, fontsize=15)
    plt.tight_layout()

    plt.savefig(plot_file)
    plt.clf()

if __name__ == "__main__":

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
    f12 = "/Users/angela/src/private/mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-313"
    plot_file = "plots/frame-rate/frame-rate-afn-models.pdf"
    plot_models([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12],
         ["0", "4", "17", "18", "41", "87", "165", "197", "229", "249", "280", "313"], plot_file)

    plot_file = "plots/frame-rate/frame-rate-afn-slo.pdf"
    plot_slos(f5, plot_file)

