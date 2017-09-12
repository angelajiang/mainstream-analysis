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
    for i in range(2): # Hack to get dimensions to match between 1st and 2nd graph
        cycol = cycle('rcgmbrk').next
        for accuracy_file, label in \
                zip(accuracy_files, labels):

            acc_data, indices = get_accuracy_data(accuracy_file)
            ys  = [acc_data[index] for index in indices]

            plt.scatter(indices, ys, s=35, color=cycol(), edgecolor='black', label=label)

            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            #plt.tick_params(axis='x', which='major', labelsize=28)
            #plt.tick_params(axis='x', which='minor', labelsize=20)

            plt.xlim(0, 350)
            plt.ylim(.2, 1)

            plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
            plt.xlabel("More frozen layers ->", fontsize=28)
            plt.ylabel("Top-1 Accuracy", fontsize=28)
            plt.legend(loc=4, fontsize=20)
            #plt.gca().invert_xaxis()
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)
            plt.tight_layout()

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

    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"
    accuracy_file2 = "output/mainstream/accuracy/flowers/resnet/flowers-40-0.0001-chokepoints"
    accuracy_file3 = "output/mainstream/accuracy/flowers/mobilenets/flowers-40-0.0001"
    accuracy_file4 = "output/mainstream/accuracy/paris/resnet/paris-40-0.0001-chokepoints"

    accuracy_files = [accuracy_file1, accuracy_file2, accuracy_file3, accuracy_file4]
    labels = ["Flowers-InceptionV3", "Flowers-ResNet50", "Flowers-Mobilenets-224", "Paris-ResNet50"]
    plot_file = "plots/accuracy/accuracy-by-layer.pdf"

    plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

