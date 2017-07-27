import pprint as pp
import math
import sys
import math
import matplotlib
import numpy as np
from scipy.stats import linregress


matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def get_latency_data(csv_file, num_apps):
    data = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_NN = int(vals[1])
            if (num_NN == num_apps):
                base = float(vals[4])
                task = float(vals[5])
                total = base + task
                data.append(total)
    return data

def get_resnet_data(csv_file):
    speeds = {"pascal":[], "ti1080":[], "maxwell":[]}
    accuracies = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            dnn = vals[0]
            top1_error = float(vals[1])
            pascal = float(vals[2])
            ti1080 = float(vals[3])
            maxwell = float(vals[4])
            accuracies.append((1 - (top1_error / 100)))
            speeds["pascal"].append(pascal)
            speeds["ti1080"].append(ti1080)
            speeds["maxwell"].append(maxwell)
    return speeds, accuracies

modes = ["resnet-pascal", "resnet-maxwell", "huang", "flowers", "trains"]
modes = ["trains"]
for mode in modes:

    resnet_speeds, resnet_accuracies = get_resnet_data("output/related_work/johnson-benchmarks-resnet.csv")
    if (mode == "resnet-pascal"):
        speed = resnet_speeds["pascal"]
        Y = resnet_accuracies

    if (mode == "resnet-maxwell"):
        speed = resnet_speeds["maxwell"]
        Y = resnet_accuracies

    if (mode == "huang"):
        speed = [60, 105]
        Y = [.71, .78]

    if (mode == "flowers"):
        speed = get_latency_data("output/streamer/latency/latency-processors-throttled.csv", 4)
        Y = [.8121, .8121, .8203, .8203, .8162, .8189, .8217, .8189, .8162, .8148, 
             .8107, .8217, .8203, .8121, .8176, .8189, .8669, .8477, .7380, .2346]
        print speed, Y

    if (mode == "trains"):
        speed = get_latency_data("output/streamer/latency/latency-processors-throttled.csv", 4)
        Y = [.9855, .9855, .9831, .9879, .9879, .9879, .9831, .9831, .9831, .9831,
             .9831, .9831, .9831, .9831, .9855, .9952, .9952, .9831, .9080, .6610]

        print speed
        speed = [192.316, 164.831]
        Y = [.9831, .9080]

    X = [math.log(s) for s in speed]
    linreg = linregress(X, Y)

    print mode, linreg.slope, linreg.rvalue

    plt.scatter(X, Y, s=50, color="darkorchid", edgecolor='black', linewidth='0.5')

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.xlabel("Log latency (ms)", fontsize=20)
    plt.ylabel("Top-1 Accuracy", fontsize=20)
    plt.title(mode, fontsize=30)
    plt.tight_layout()
    plt.savefig("plots/tradeoffs/linearized-" + mode + ".pdf")
    plt.clf()

