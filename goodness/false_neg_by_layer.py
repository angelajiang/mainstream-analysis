import pprint as pp
import math
import sys
sys.path.append('include/')
import matplotlib
import numpy as np
from itertools import cycle
import matplotlib.pyplot as plt

import layers_info

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def op_to_layer(op_full):
    tensor_name = (op_full.split(":"))[0]
    layer = tensor_name.split("/")[0]
    return layer

def get_layers(csv_file, layers_index):
    layers = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[layers_index]
            layer = op_to_layer(op_full)
            if layer not in layers:
                layers.append(layer)
    return layers

def get_num_NNs(csv_file):
    num_NNs = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_NN = int(vals[1])
            if num_NN not in num_NNs:
                num_NNs.append(num_NN)
    return num_NNs

def get_throughput_data(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
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

def get_probability_miss(p_identified, min_event_length_ms, max_fps, observed_fps):
    stride = max_fps / float(observed_fps)
    d = min_event_length_ms / float(1000) * max_fps
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
    print p_miss
    return p_miss

def plot_false_negative_rate(arch, latency_file, accuracy_file, min_event_length_ms, max_fps, plot_dir):
    num_NNs = get_num_NNs(latency_file)
    for i in range(2): # Hack to get dimensions to match between 1st and 2nd graph
        cycol = cycle('rcmkbgy').next
        for num_NN in num_NNs:
            layers = get_layers(latency_file, 0)

            throughput_data = get_throughput_data(latency_file)
            acc_data = get_accuracy_data(arch, accuracy_file)

            xs  = range(0, len(layers))
            throughputs  = [throughput_data[num_NN][layer]["task"] for layer in layers]
            accuracies  = [acc_data[layer] for layer in layers]

            ys = []
            for fps, acc in zip(throughputs, accuracies):
                p_miss = get_probability_miss(acc, min_event_length_ms, max_fps, fps)
                ys.append(p_miss)

            plt.scatter(xs, ys, s=20, color=cycol(), edgecolor='black', label=str(num_NN)+" apps")
            plt.xticks(xs, layers, rotation="vertical")

            plt.tick_params(axis='y', which='major', labelsize=24)
            plt.tick_params(axis='y', which='minor', labelsize=20)

            plt.ylim(0, 1)

            plt.ylabel("False negative rate", fontsize=20)
            plt.legend(loc=0, fontsize=15)
            plt.tight_layout()
        plt.savefig(plot_dir +"/prob-miss" + str(min_event_length_ms) + ".pdf")
        plt.clf()

if __name__ == "__main__":

    arch1 = "iv3"
    latency_file1 = "output/streamer/throughput/inception/flow_control/multi-app"
    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"

    plot_dir = "plots/goodness/"

    plot_false_negative_rate(arch1, latency_file1, accuracy_file1, 500, 30, plot_dir)
    #plot_false_negative_rate(arch1, latency_file1, accuracy_file1, 200, 5, plot_dir)

