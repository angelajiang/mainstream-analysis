import pprint as pp
import sys
import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def op_to_layer(op_full):
    tensor_name = (op_full.split(":"))[0]
    layer = tensor_name.split("/")[0]
    return layer

def plot_sizes(csv_file):
    layers = []
    ys = []
    width = .5
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            d1 = int(vals[1])
            d2 = int(vals[2])
            d3 = int(vals[3])
            layer = op_to_layer(op_full)
            layers.append(layer)
            ys.append(d1*d2*d3*4 / 1000)
    xs = range(len(ys))
    plt.bar(xs, ys, width=width, color="lightcoral")
    ind = np.arange(len(ys))
    plt.xticks(ind + width / 2, layers, rotation="vertical")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.ylabel("Output size in KB", fontsize=28)
    plt.tight_layout()
    plt.savefig("plots/sizes.pdf")

if __name__ == "__main__":
    csv_file = sys.argv[1]
    plot_sizes(csv_file)
