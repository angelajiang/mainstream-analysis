# -*- coding: utf-8 -*-
import pprint as pp
import sys
import matplotlib
import numpy as np

sys.path.append('scripts/util/')
import preprocess
import plot_util

sys.path.append('include')
import layers_info

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

do_flip = False
if do_flip:
    more_sharing_label = "No. of unspecialized layers"
else:
    # more_sharing_label = u"More sharing →"
    more_sharing_label = u"% of shared layers"
do_norm = True

# CSV file needs to be of format
# layer1,camera_fps,transformer_fps,base_fps,task_fps
# layer2,camera_fps,transformer_fps,base_fps,task_fps
LAYERS = ["input_1",
          "conv2d_1/convolution",
          "conv2d_2/convolution",
          "conv2d_3/convolution",
          "conv2d_1/convolution",
          "conv2d_2/convolution",
          "conv2d_3/convolution",
          "max_pooling2d_1/MaxPool",
          "conv2d_4/convolution",
          "conv2d_5/convolution",
          "max_pooling2d_2/MaxPool",
          "mixed0/concat",
          "mixed1/concat",
          "mixed2/concat",
          "mixed3/concat",
          "mixed4/concat",
          "mixed5/concat",
          "mixed6/concat",
          "mixed7/concat",
          "mixed8/concat",
          "mixed9/concat",
          "mixed10/concat"]
          #"dense_2/Softmax:0"]

MARKERS = ["o", "h", "D", "x", "1", "*", "p","8"]

def get_data(csv_file, net_info, experiment_name):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = preprocess.op_to_layer(op_full)
            num_frozen = preprocess.layer_to_number(layer, net_info)

            num_NN = int(vals[1])
            base = float(vals[2])
            tasks = [float(i) for i in vals[3:]]
            task_avg = np.average(tasks)
            if num_NN not in data.keys():
                data[num_NN] = {}
            if layer not in data[num_NN].keys():
                data[num_NN][num_frozen] = {"base": [], "task":[]}

            if experiment_name == "throughput":
                if len(tasks) == 0:
                    task_avg = base
                if base == 0:
                    base = task_avg

            data[num_NN][num_frozen]["base"].append(base)
            data[num_NN][num_frozen]["task"].append(task_avg)
    return data

def plot_throughput(csv_file, net_info, plot_dir):
    num_NNs = preprocess.get_num_NNs(csv_file)
    num_frozens = preprocess.get_num_frozens(csv_file, 0, net_info)
    data = get_data(csv_file, net_info, "throughput")
    max_layers = net_info["num_layers"]

    xs = num_frozens
    if do_flip:
        xs = list(reversed(xs))
    if do_norm:
        xs = [int(round(x*100. / max_layers)) for x in xs]

    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN, marker, c in zip(num_NNs, MARKERS, plot_util.COLORLISTS[5]):
            task_fps = [np.average(data[num_NN][num_frozen]["task"]) for num_frozen in num_frozens]
            plt.plot(xs, task_fps, marker=marker, label=str(num_NN)+" apps", lw=4, markersize=8, color=c)

        # Format plot
        plt.xlabel(more_sharing_label, fontsize=25)
        # plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
        plt.ylabel("Throughput (FPS)", fontsize=28)

        plt.tick_params(axis='y', which='major', labelsize=30)
        plt.tick_params(axis='y', which='minor', labelsize=24)
        plt.tick_params(axis='x', which='major', labelsize=30)
        plt.tick_params(axis='x', which='minor', labelsize=24)
        plt.ylim(0,6)
        if do_norm:
            plt.xlim(0, 115)
        else:
            plt.xlim(1, max_layers + 4)

        if do_flip:
            plt.legend(loc=0, fontsize=20, frameon=True)
        else:
            plt.legend(loc=4, fontsize=20)
        plt.gca().xaxis.grid(True)
        plt.gca().yaxis.grid(True)
        plt.tight_layout()
        plt.savefig(plot_dir + "/task-throughput-partial.pdf")

        plt.clf()

def plot_latency(processors_file, net_info, plot_dir):
    layers = preprocess.get_layers(processors_file, 0)
    num_frozens = preprocess.get_num_frozens(csv_file, 0, net_info)
    num_NNs = preprocess.get_num_NNs(processors_file)
    max_layers = net_info["num_layers"]
    data = get_data(processors_file, net_info, "latency-processors")
    width = 0.8

    xs = num_frozens
    if do_flip:
        xs = list(reversed(xs))
    if do_norm:
        xs = [int(round(x*100. / max_layers)) for x in xs]


    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:

            base_fps = [np.average(data[num_NN][num_frozen]["base"]) for num_frozen in num_frozens]
            task_fps = [np.average(data[num_NN][num_frozen]["task"]) for num_frozen in num_frozens]
            base_errs = [np.std(data[num_NN][num_frozen]["base"]) for num_frozen in num_frozens]
            task_errs = [np.std(data[num_NN][num_frozen]["task"]) for num_frozen in num_frozens]

            plt.bar(xs, base_fps, width, yerr=base_errs,
                    label="Shared NNE",
                    color=plot_util.NO_SHARING["color"],
                    hatch=plot_util.NO_SHARING["pattern"],
                    error_kw={'ecolor':'green', 'linewidth':3})

            plt.bar(xs, task_fps, width, bottom=base_fps, yerr=task_errs,
                    label="Task NNE",
                    color=plot_util.MAINSTREAM["color"],
                    hatch=plot_util.MAINSTREAM["pattern"],
                    error_kw={'ecolor':'green', 'linewidth':3})

            plt.xlabel(more_sharing_label, fontsize=28)
            plt.ylabel("CPU per frame (ms)", fontsize=28)
            plt.ylim(0, 1000)
            plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.legend(loc=0, fontsize=20, ncol=2)
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)
            plt.title(str(num_NN) + " NNs", fontsize=30)
            plt.tight_layout()
            plot_file = plot_dir + "/latency-" + str(num_NN) + "-NN.pdf"
            plt.savefig(plot_file)
            plt.clf()

if __name__ == "__main__":
    plot_dir = "plots/performance/throughput/inception/flow_control"
    csv_file = "output/streamer/throughput/inception/flow_control/multi-app"
    net_info = layers_info.inception_info

    plot_dir = "plots/performance/throughput/yolo/flow_control"
    csv_file = "output/streamer/throughput/yolo/throughput.csv"
    net_info = layers_info.yolo_info
    plot_throughput(csv_file, net_info, plot_dir)
    csv_file = "output/streamer/latency/yolo/latency.csv"
    plot_latency(csv_file, net_info, plot_dir)

