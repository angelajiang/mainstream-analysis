import pprint as pp
import sys
sys.path.append('include/')
import matplotlib
import numpy as np
from itertools import cycle
from scipy.interpolate import PchipInterpolator

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


def get_max_fps_data(csv_file):
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

            data[num_NN][layer]["total"] = 1 / (float(task + base) / 1000)
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


def plot_accuracy_vs_fps(arches, latency_files, accuracy_files, labels, plot_dir):
    num_NNs = get_num_NNs(latency_files[0])

    for i in range(2):  # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            cycol = cycle('rcmkbg').next
            cymark = cycle('ovDxh1*').next
            all_pts = []
            pts_by_net = {}
            for arch, latency_file, accuracy_file, label in \
                    zip(arches, latency_files, accuracy_files, labels):
                layers = get_layers(latency_file, 0)

                latency_data = get_max_fps_data(latency_file)
                acc_data = get_accuracy_data(arch, accuracy_file)

                xs = [latency_data[num_NN][layer]["total"] for layer in layers]
                ys = [acc_data[layer] for layer in layers]

                all_pts += list(zip(xs, ys))
                pts_by_net[label] = list(zip(xs, ys))

                plt.scatter(xs, ys, s=60, marker=cymark(), color=cycol(), edgecolor='black', label=label)

            pts = []
            highest = -1
            for x, y in sorted(all_pts, reverse=True):
                if y > highest:
                    highest = y
                    pts.append((x, y))
            pts = sorted(pts)
            xs, ys = zip(*pts)

            all_xs = [pt[0] for pt in all_pts]

            xss = np.linspace(min(all_xs), max(all_xs), 100)

            spl = PchipInterpolator(xs, ys)
            ys = spl(xss)

            plt.plot(xss, ys, '--', label='Frontier')

            pt_a = sorted(pts_by_net['MobileNets-224'])[0]
            # B: Closest point on Inception curve above A.
            pt_b = sorted(pts_by_net["InceptionV3"], key=lambda x: abs(pt_a[0] - x[0]))[0]

            print(pt_a, pt_b)
            plt.annotate("A: Run 4 full MobileNets",
                         xy=pt_a,
                         xytext=(-20, -90),
                         xycoords='data',
                         fontsize=20,
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle="->", connectionstyle="angle3,angleA=105,angleB=10", relpos=(.02, .5)))

            plt.annotate("B: Share partial InceptionV3s",
                         xy=pt_b,
                         xytext=(+30, 10),
                         xycoords='data',
                         fontsize=20,
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle="->", connectionstyle="angle3,angleA=0,angleB=55", relpos=(0, .5)))
            
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=24)
            plt.tick_params(axis='x', which='major', labelsize=28)
            plt.tick_params(axis='x', which='minor', labelsize=24)

            plt.ylim(0, 1)

            plt.xlabel("Throughput (FPS)", fontsize=30)
            plt.ylabel("Top-1 Accuracy", fontsize=30)
            plt.legend(loc=4, fontsize=20)
            #plt.title(str(num_NN) + " applications", fontsize=30)
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)
            plt.tight_layout()
            plt.savefig(plot_dir + "/acc-fps-" + str(num_NN) + "-NN.pdf")
            plt.clf()


if __name__ == "__main__":

    arch1 = "iv3"
    arch2 = "r50"
    arch3 = "mnets"

    latency_file1 = "output/streamer/latency/inception/basic/latency-processors-iv3.csv"
    latency_file2 = "output/streamer/latency/resnet/basic/latency-processors-r50.csv"
    latency_file3 = "output/streamer/latency/mobilenets/basic/latency.csv"

    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"
    accuracy_file2 = "output/mainstream/accuracy/flowers/resnet/flowers-40-0.0001-chokepoints"
    accuracy_file3 = "output/mainstream/accuracy/flowers/mobilenets/flowers-40-0.0001"

    arches = [arch1, arch2, arch3]
    latency_files = [latency_file1, latency_file2, latency_file3]
    accuracy_files = [accuracy_file1, accuracy_file2, accuracy_file3]
    labels = ["InceptionV3", "ResNet50", "MobileNets-224"]

    plot_dir = "plots/tradeoffs/flowers"

    plot_accuracy_vs_fps(arches, latency_files, accuracy_files, labels, plot_dir)
