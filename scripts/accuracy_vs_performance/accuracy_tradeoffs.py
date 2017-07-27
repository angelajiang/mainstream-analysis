import pprint as pp
import sys
sys.path.append('include/')
import matplotlib
import numpy as np
from itertools import cycle

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

def get_latency_data(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
            num_NN = int(vals[1])
            base = float(vals[4])
            task = float(vals[5])
            if num_NN not in data.keys():
                data[num_NN] = {}
            if layer not in data[num_NN].keys():
                data[num_NN][layer] = {}

            data[num_NN][layer]["base"] = base
            data[num_NN][layer]["task"] = task
            data[num_NN][layer]["total"] = base + task
    return data

def get_accuracy_data(architecture, csv_file):
    if architecture == "iv3":
        layer_names = layers_info.InceptionV3_Layer_Names
    elif architecture == "r50":
        layer_names = layers_info.ResNet50_Layer_Names

    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            frozen_index = int(vals[0])
            acc = float(vals[1])
            layer = layer_names[frozen_index]
            data[layer] = acc
    return data

def plot_accuracy_vs_ms(arch, latency_files, accuracy_files, labels, plot_dir):
    num_NNs = get_num_NNs(latency_files[0])
    for i in range(2): # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            cycol = cycle('rcmkbg').next
            for arch, latency_file, accuracy_file, label in \
                    zip(arches, latency_files, accuracy_files, labels):
                layers = get_layers(latency_file, 0)

                latency_data = get_latency_data(latency_file)
                acc_data = get_accuracy_data(arch, accuracy_file)

                xs  = [latency_data[num_NN][layer]["total"] for layer in layers]
                ys  = [acc_data[layer] for layer in layers]

                plt.scatter(xs, ys, s=50, color=cycol(), edgecolor='black', label=label)

                plt.tick_params(axis='y', which='major', labelsize=28)
                plt.tick_params(axis='y', which='minor', labelsize=20)
                plt.tick_params(axis='x', which='major', labelsize=28)
                plt.tick_params(axis='x', which='minor', labelsize=20)

                plt.xlim(150, 375)
                plt.ylim(.2, 1)

                plt.xlabel("Latency (ms)", fontsize=20)
                plt.ylabel("Top-1 Accuracy", fontsize=20)
                plt.legend(loc=4, fontsize=15)
                plt.title(str(num_NN) + " apps", fontsize=30)
                plt.tight_layout()
                plt.savefig(plot_dir +"/acc-ms-"+str(num_NN)+"-NN.pdf")
            plt.clf()


if __name__ == "__main__":

    arch1 = "iv3"
    arch2 = "r50"

    latency_file1 = "output/streamer/latency/latency-processors-iv3.csv"
    latency_file2 = "output/streamer/latency/latency-processors-r50.csv"

    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"
    accuracy_file2 = "output/mainstream/accuracy/flowers/resnet/flowers-40-0.0001-chokepoints"

    arches = [arch1, arch2]
    latency_files = [latency_file1, latency_file2]
    accuracy_files = [accuracy_file1, accuracy_file2]
    labels = ["InceptionV3", "ResNet50"]

    plot_dir = "plots/tradeoffs/flowers"

    plot_accuracy_vs_ms(arches, latency_files, accuracy_files, labels, plot_dir)

