import pprint as pp
import sys
import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

# CSV file needs to be of format
# layer1,camera_fps,transformer_fps,base_fps,task_fps
# layer2,camera_fps,transformer_fps,base_fps,task_fps

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

def get_accuracy_data(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[1]
            layer = op_to_layer(op_full)
            acc = float(vals[2])
            data[layer] = acc
    return data

def plot_accuracy_vs_speedup(latency_file, accuracy_file, plot_dir):
    layers = get_layers(latency_file, 0)
    layers2 = get_layers(accuracy_file, 1)

    assert layers == layers2

    num_NNs = get_num_NNs(latency_file)
    latency_data = get_latency_data(latency_file)
    acc_data = get_accuracy_data(accuracy_file)
    width = 0.4
    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            xs = range(len(layers))

            speeds  = [latency_data[num_NN][layer]["total"] for layer in layers]
            accuracies  = [acc_data[layer] for layer in layers]

            fig, ax = plt.subplots()
            ax.scatter(speeds, accuracies)
            for i, label in enumerate(layers):
                ax.annotate(label, (speeds[i], accuracies[i]), rotation=270)
            #ax.set_yscale('log')
            ax.set_title(str(num_NN) + " NNs", fontsize=30)
            ax.set_xlabel("Speed (ms)", fontsize=20)
            ax.set_ylabel("Accuracy", fontsize=20)
            ax.set_xlim([150, 375])
            ax.set_ylim([.2, .9])

            [tick.label.set_fontsize(20) for tick in ax.yaxis.get_major_ticks()]
            [tick.label.set_fontsize(20) for tick in ax.xaxis.get_major_ticks()]


            '''
            plt.xticks(xs, layers, rotation="vertical")
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.legend(loc=0, fontsize=15, ncol=2)
            plt.ylabel("Processor Latency (ms)", fontsize=20)
            plt.title(str(num_NN) + " NNs", fontsize=30)
            '''
            plt.tight_layout()
            plt.savefig(plot_dir +"/acc-speed-"+str(num_NN)+"-NN.pdf")
            plt.clf()


if __name__ == "__main__":
    latency_file = sys.argv[1]
    accuracy_file = sys.argv[2]
    plot_dir = sys.argv[3]
    plot_accuracy_vs_speedup(latency_file, accuracy_file, plot_dir)

