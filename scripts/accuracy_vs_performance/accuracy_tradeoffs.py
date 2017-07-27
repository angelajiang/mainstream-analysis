import pprint as pp
import sys
sys.path.append('include/')
import matplotlib
import numpy as np

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
    if architecture == "inceptionv3":
        layer_names = layers_info.InceptionV3_Layer_Names
    elif architecture == "resnet50":
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

def plot_accuracy_vs_speedup(architecture, latency_file, accuracy_file, plot_dir):
    layers = get_layers(latency_file, 0)

    num_NNs = get_num_NNs(latency_file)
    latency_data = get_latency_data(latency_file)
    acc_data = get_accuracy_data(architecture, accuracy_file)
    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:

            xs  = [latency_data[num_NN][layer]["total"] for layer in layers]
            ys  = [acc_data[layer] for layer in layers]

            plt.scatter(xs, ys, s=30, color="darkorchid", edgecolor='black', linewidth='0.5')

            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.tick_params(axis='x', which='major', labelsize=28)
            plt.tick_params(axis='x', which='minor', labelsize=20)

            if num_NN  > 3:
                for label, x, y in zip(layers, xs, ys):
                    plt.annotate(
                        label,
                        fontsize=8,
                        xy=(x, y),
                        #arrowprops=dict(arrowstyle = '->', connectionstyle='arc3,rad=0'),
                        rotation=45)

            plt.xlim(150, 375)
            plt.ylim(.2, 1)

            plt.xlabel("Latency (ms)", fontsize=20)
            plt.ylabel("Top-1 Accuracy", fontsize=20)
            plt.title(str(num_NN) + " apps", fontsize=30)
            plt.tight_layout()
            plt.savefig(plot_dir +"/acc-speed-"+str(num_NN)+"-NN.pdf")
            plt.clf()


if __name__ == "__main__":
    architecture = sys.argv[1]
    latency_file = sys.argv[2]
    accuracy_file = sys.argv[3]
    plot_dir = sys.argv[4]
    plot_accuracy_vs_speedup(architecture, latency_file, accuracy_file, plot_dir)

