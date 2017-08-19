import pprint as pp
import math
import sys
import matplotlib
import numpy as np
import random
from itertools import cycle
import matplotlib.pyplot as plt

sys.path.append('include/')
import layers_info
sys.path.append('scripts/util/')
import preprocess

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def get_throughput_data(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = preprocess.op_to_layer(op_full)
            num_NN = int(vals[1])
            base = float(vals[2])
            tasks = [float(t) for t in vals[3:]]
            task = np.average(tasks)

            if num_NN not in data.keys():
                data[num_NN] = {}
            if layer not in data[num_NN].keys():
                data[num_NN][layer] = {}

            if (task == 0):
                task = base

            data[num_NN][layer]["base"] = base
            data[num_NN][layer]["task"] = task
    return data

def get_accuracy_data(architecture, csv_file):
    if architecture == "iv3":
        layer_names = layers_info.InceptionV3_Layer_Names
    elif architecture == "r50":
        layer_names = layers_info.ResNet50_Layer_Names
    elif architecture == "mnets":
        layer_names = layers_info.MobileNets_Layer_Names

    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            frozen_index = int(vals[0])
            acc = float(vals[1])
            layer = layer_names[frozen_index]
            data[layer] = acc
    return data

def get_probability_miss(p_identified_list, min_event_length_ms, max_fps, observed_fps):
    stride = max_fps / float(observed_fps)
    d = min_event_length_ms / float(1000) * max_fps
    p_misses = []
    for p_identified in p_identified_list:
        if d < 1:
            print "Event of length", min_event_length_ms, "ms cannot be detected at", max_fps, "FPS"
            p_miss = 1
        elif d < stride:
            p_encountered = d / stride
            p_hit = p_encountered * p_identified
            p_miss = 1 - p_hit
        else:
            mod = (d % stride)
            p1 = (d - (mod)) / d
            r1 = math.floor(d / stride)
            p2 = mod / d
            r2 = math.ceil(d / stride)
            p_not_identified = 1 - p_identified
            p_miss = p1 * math.pow(p_not_identified, r1) + \
                        p2 * math.pow(p_not_identified, r2)
        p_misses.append(p_miss)
    return np.average(p_misses)

def plot_false_negative_rate(arch, latency_file, accuracy_file, sigma, num_events, min_event_length_ms, max_fps, plot_dir):
    num_NNs = preprocess.get_num_NNs(latency_file)
    shapes = ["o", "h", "D", "x", "1", "*", "P", "8"]
    for i in range(2): # Hack to get dimensions to match between 1st and 2nd graph
        cycol = cycle('rcmkbgy').next
        for num_NN, marker in zip(num_NNs[3:7], shapes):
            layers = preprocess.get_layers(latency_file, 0)

            throughput_data = get_throughput_data(latency_file)
            acc_data = get_accuracy_data(arch, accuracy_file)

            xs  = range(0, len(layers))
            throughputs  = [throughput_data[num_NN][layer]["task"] for layer in layers]
            accuracies  = [acc_data[layer] for layer in layers]

            ys = []
            for fps, acc in zip(throughputs, accuracies):
                acc_dist = [random.gauss(acc, sigma) for i in range(num_events)]
                p_miss = get_probability_miss(acc_dist, min_event_length_ms, max_fps, fps)
                ys.append(p_miss)

            plt.scatter(xs, ys, s=50, marker=marker, color=cycol(), edgecolor='black', label=str(num_NN)+" apps")

            plt.xlabel("More sharing ->", fontsize=28)
            plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
            plt.tick_params(axis='y', which='major', labelsize=24)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.ylim(0, 0.6)
            plt.ylabel("False negative rate", fontsize=28)

            plt.title("Sigma = " + str(sigma), fontsize=30)
            plt.legend(loc=0, fontsize=15)
            plt.tight_layout()

        plt.savefig(plot_dir +"/false-neg-" + \
                                str(min_event_length_ms) + "ms-" + \
                                str(sigma) + "sig-" + \
                                str(max_fps) + "fps.pdf")
        plt.clf()

if __name__ == "__main__":

    arch1 = "iv3"
    latency_file1 = "output/streamer/throughput/inception/flow_control/multi-app"
    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"

    plot_dir = "plots/goodness/"

    plot_false_negative_rate(arch1, latency_file1, accuracy_file1, 0, 10, 300, 30, plot_dir)
    plot_false_negative_rate(arch1, latency_file1, accuracy_file1, .1, 10, 300, 30, plot_dir)
    plot_false_negative_rate(arch1, latency_file1, accuracy_file1, .2, 10, 300, 30, plot_dir)
    plot_false_negative_rate(arch1, latency_file1, accuracy_file1, .4, 10, 300, 30, plot_dir)

