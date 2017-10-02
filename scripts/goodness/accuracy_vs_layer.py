# -*- coding: utf-8 -*-
import pprint as pp
import sys
sys.path.append('include/')
import matplotlib
import numpy as np
from itertools import cycle
import layers_info
sys.path.append('scripts/util/')
import plot_util as util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

do_flip = False
num_layers = 314
do_norm = True

def get_num_NNs(csv_file):
    num_NNs = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_NN = int(vals[1])
            if num_NN not in num_NNs:
                num_NNs.append(num_NN)
    return num_NNs

def get_accuracy_data(csv_file):
    data = {}
    indices = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            frozen_index = int(vals[0])
            acc = float(vals[1])
            data[frozen_index] = acc
            indices.append(frozen_index)
    return data, indices

def plot_accuracy_vs_layer(accuracy_files, labels, plot_file):
    cs = util.COLORLISTS[12]
    markers = ["o", "h", "D"]
    for i in range(2): # Hack to get dimensions to match between 1st and 2nd graph
        ci = 0
        mi = 0
        for accuracy_file, label in \
                zip(accuracy_files, labels):

            mindex = mi % len(markers)
            acc_data, indices = get_accuracy_data(accuracy_file)
            ys  = [acc_data[index] for index in indices]

            #plt.scatter(indices, ys, s=35, color=cycol(), edgecolor='black', label=label)
            num_layers = max(indices) + 1
            if do_norm:

                indices = [int(round(x * 100. / num_layers)) for x in indices]
            else:
                indices = [num_layers - x for x in indices]
            plt.plot(indices, ys, linestyle="--", marker=markers[mindex], color=cs[ci], lw=2, label=label)

            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.tick_params(axis='x', which='major', labelsize=28)
            plt.tick_params(axis='x', which='minor', labelsize=20)

            if not do_norm:
                plt.xlim(0, 350)
            else:
                plt.xlim(0, 102)
            plt.ylim(0, 1)

            # plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')

            if do_norm:
                plt.xlabel("% of layers that are unspecialized", fontsize=30)
            elif do_flip:
                plt.xlabel("No. of unspecialized layers", fontsize=30)
            else:
                plt.xlabel(u"Fewer specialized layers →", fontsize=30)
            plt.ylabel("Top-1 Accuracy", fontsize=30)
            plt.legend(loc=0, fontsize=15, frameon=not do_norm)
            #plt.gca().invert_xaxis()
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)
            plt.tight_layout()
            ci += 1
            mi += 1

        plt.savefig(plot_file)
        plt.clf()

if __name__ == "__main__":

    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-nodropout"
    accuracy_file2 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dataaug"
    accuracy_file3 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"

    accuracy_files = [accuracy_file1, accuracy_file2, accuracy_file3]
    labels = ["Basic", "Data Aug", "Dropout"]
    plot_file = "plots/accuracy/overfit.pdf"

    plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

    fi = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"
    fr = "output/mainstream/accuracy/flowers/resnet/flowers-40-0.0001-chokepoints"
    fm = "output/mainstream/accuracy/flowers/mobilenets/flowers-40-0.0001"
    pr = "output/mainstream/accuracy/paris/resnet/paris-40-0.0001-chokepoints"
    pi = "output/mainstream/accuracy/paris/inception/paris-40-0.0001-dropout"
    pm = "output/mainstream/accuracy/paris/mobilenets/paris-40-0.0001"
    ci = "output/mainstream/accuracy/cats/cats-inception-accuracy"
    cm = "output/mainstream/accuracy/cats/cats-mobilenets-accuracy"
    cr = "output/mainstream/accuracy/cats/cats-resnet-accuracy"

    accuracy_files = [fr, pr, cr, fi, pi, ci, fm, pm, cm]

    labels = [
              "Flowers-ResNet50",
              "Paris-ResNet50",
              "Cats-ResNet50",
              "Flowers-InceptionV3",
              "Paris-InceptionV3",
              "Cats-InceptionV3",
              "Flowers-MobileNets-224",
              "Paris-MobileNets-224",
              "Cats-MobileNets-224",
              ]
    plot_file = "plots/accuracy/accuracy-by-layer.pdf"

    plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

