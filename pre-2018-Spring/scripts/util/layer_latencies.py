import pprint as pp
import sys
sys.path.append('include/')
import layers_info
sys.path.append('scripts/util/')
import plot_util

import matplotlib
import numpy as np

#matplotlib.use('Agg')
import matplotlib.pyplot as plt
# matplotlib.style.use('classic')
#plt.ioff()

def op_to_layer(op_full):
    tensor_name = (op_full.split(":"))[0]
    layer = tensor_name.split("/")[0]
    return layer

def print_and_plot_latencies(csv_file, layer_names, label, plot_dir):
    data = {}

    layers = []
    last_total_latency = 0
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            total_latency = float(vals[2])
            layer = op_to_layer(op_full)
            if layer not in data.keys():
                data[layer] = []
                layers.append(layer)
            data[layer].append(total_latency)

    last_avg_latency = 0
    last_layer_number = 0

    layer_latencies = []
    ys = []
    errs = []

    for layer in layers:
        total_latencies = data[layer]
        latencies = [l - last_avg_latency for l in total_latencies]

        # Data for plot
        avg_latency = round(np.average(latencies), 4)
        err = np.std(latencies)
        ys.append(avg_latency)
        errs.append(err)

        # Data for print
        ls= [name for num, name in layer_names.iteritems()]
        layer_number = [num for num, name in layer_names.iteritems() if name == layer][0]
        layers_in_seg = layer_number - last_layer_number

        arr = [avg_latency / float(layers_in_seg)] * (layers_in_seg)
        layer_latencies += arr

        last_avg_latency += avg_latency
        last_layer_number = layer_number

    max_latency = max(layer_latencies)
    normalized_latencies = [round(l / float(max_latency), 4) for l in layer_latencies]

    width = 0.75
    plt.clf()
    xs = range(len(ys))
    plt.bar(xs, ys, width, yerr=err,
            color=plot_util.NO_SHARING["color"],
            hatch=plot_util.NO_SHARING["pattern"],
            zorder=3,
            error_kw={'ecolor':'green', 'linewidth':3})

    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
    plt.xlim(0, max(xs))
    plt.ylim(0, 25)
    plt.gca().yaxis.grid(True)
    plt.xlabel("Subgraph", fontsize=30)
    plt.ylabel("Forward-pass latency (ms)", fontsize=25)
    plt.tight_layout()
    plt.savefig(plot_dir + "/latency-by-layer-" + label + ".pdf")

    # print normalized_latencies

if __name__ == "__main__":
    csv_file = "output/streamer/latency/inception/basic/latency-by-layer.csv"
    layer_names = layers_info.InceptionV3_Layer_Names
    plot_dir = "plots/performance/latency/inception/basic/"
    print_and_plot_latencies(csv_file, layer_names, "InceptionV3", plot_dir)

    csv_file = "output/streamer/latency/mobilenets/basic/latency-by-layer.csv"
    layer_names = layers_info.MobileNets_Layer_Names
    plot_dir = "plots/performance/latency/mobilenets/basic/"
    print_and_plot_latencies(csv_file, layer_names, "MobileNets-224", plot_dir)

    csv_file = "output/streamer/latency/resnet/basic/latency-by-layer.csv"
    layer_names = layers_info.ResNet50_Layer_Names
    plot_dir = "plots/performance/latency/resnet/basic/"
    print_and_plot_latencies(csv_file, layer_names, "ResNet-50", plot_dir)
