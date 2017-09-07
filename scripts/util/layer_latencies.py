import pprint as pp
import sys
sys.path.append('include/')
import layers_info

import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def op_to_layer(op_full):
    tensor_name = (op_full.split(":"))[0]
    layer = tensor_name.split("/")[0]
    return layer

def print_latencies(csv_file):
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

    layer_names = layers_info.MobileNets_Layer_Names

    last_avg_latency = 0
    last_layer_number = 0

    layer_latencies = []

    for layer in layers:
        total_latencies = data[layer]
        avg_total_latency = np.average(total_latencies)
        avg_latency = round(avg_total_latency - last_avg_latency, 4)
        layer_number = [num for num, name in layer_names.iteritems() if name == layer][0]
        arr = [avg_latency] * (layer_number - last_layer_number)

        layer_latencies += arr

        last_avg_latency = avg_latency
        last_layer_number = layer_number

    max_latency = max(layer_latencies)
    normalized_latencies = [round(l / float(max_latency), 4) for l in layer_latencies]

    print normalized_latencies

if __name__ == "__main__":
    csv_file = sys.argv[1]
    print_latencies(csv_file)
