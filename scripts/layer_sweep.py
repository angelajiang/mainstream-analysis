# -*- coding: utf-8 -*-
import pprint as pp
import sys
import matplotlib
import numpy as np

sys.path.append('scripts/util/')
import preprocess
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

do_flip = False
if do_flip:
    more_sharing_label = "No. of unspecialized layers"
else:
    # more_sharing_label = u"More sharing →"
    more_sharing_label = u"Fraction of unspecialized (shared) layers"

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

def get_data(csv_file, experiment_name):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = preprocess.op_to_layer(op_full)
            num_NN = int(vals[1])
            base = float(vals[2])
            tasks = [float(i) for i in vals[3:]]
            task_avg = np.average(tasks)
            if num_NN not in data.keys():
                data[num_NN] = {}
            if layer not in data[num_NN].keys():
                data[num_NN][layer] = {"base": [], "task":[]}

            if experiment_name == "throughput":
                if len(tasks) == 0:
                    task_avg = base
                if base == 0:
                    base = task_avg

            data[num_NN][layer]["base"].append(base)
            data[num_NN][layer]["task"].append(task_avg)
    return data

def plot_max_throughput(csv_file, plot_file):
    layers = preprocess.get_layers(csv_file, 0)
    num_NNs = preprocess.get_num_NNs(csv_file)
    data = get_data(csv_file, "throughput")
    labels = ["No sharing", "Max sharing"]

    colors = [plot_util.COLORS["red"], plot_util.COLORS["grey"]]

    fpses1 = []
    fpses2 = []
    errs1 = []
    errs2 = []

    for num_NN in num_NNs:
        fps1 = np.average(data[num_NN][layers[0]]["task"])
        err1 = np.std(data[num_NN][layers[0]]["task"])

        fps2 = np.average(data[num_NN][layers[1]]["task"]) - fps1
        err2 = np.std(data[num_NN][layers[1]]["task"])

        fpses1.append(fps1)
        fpses2.append(fps2)
        errs1.append(err1)
        errs2.append(err2)

    width = 0.5
    plt.bar(num_NNs, fpses1, width, yerr=errs1,
            label="No sharing",
            color=plot_util.NO_SHARING["color"],
            hatch=plot_util.NO_SHARING["pattern"],
            error_kw={'ecolor':'green', 'linewidth':3})

    plt.bar(num_NNs, fpses2, width, yerr=errs2, bottom=fpses1,
            label="Max sharing",
            color=plot_util.MAX_SHARING["color"],
            hatch=plot_util.MAX_SHARING["pattern"],
            error_kw={'ecolor':'green', 'linewidth':3})

    # Format plot
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.xlabel("Number of concurrent applications", fontsize=28)
    plt.ylabel("Throughput (FPS)", fontsize=28)
    plt.xlim(1, 30)
    plt.ylim(0, 20)
    plt.legend(loc=0, fontsize=15)
    plt.tight_layout()
    plt.gca().yaxis.grid(True)
    plt.savefig(plot_file)
    plt.clf()

def plot_throughput(csv_file, plot_dir):
    layers = [preprocess.op_to_layer(l) for l in LAYERS]
    num_NNs = preprocess.get_num_NNs(csv_file)
    data = get_data(csv_file, "throughput")

    xs = range(len(layers))
    if do_flip:
        xs = list(reversed(xs))

    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN, marker in zip(num_NNs, MARKERS):
            task_fps = [np.average(data[num_NN][layer]["task"]) for layer in layers]
            plt.plot(xs, task_fps, marker=marker, label=str(num_NN)+" apps", lw=2)

        # Format plot
        plt.xlabel(more_sharing_label, fontsize=25)
        plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
        plt.ylabel("Throughput (FPS)", fontsize=28)

        plt.tick_params(axis='y', which='major', labelsize=28)
        plt.tick_params(axis='y', which='minor', labelsize=20)
        plt.ylim(0,20)
        plt.xlim(1, len(layers) + 4)

        if do_flip:
            plt.legend(loc=0, fontsize=15, frameon=True)
        else:
            plt.legend(loc=4, fontsize=15)
        plt.gca().xaxis.grid(True)
        plt.gca().yaxis.grid(True)
        plt.tight_layout()
        plt.savefig(plot_dir + "/task-throughput.pdf")

        plt.clf()

    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:

            base_fps = [np.average(data[num_NN][layer]["base"]) for layer in layers]
            task_fps = [np.average(data[num_NN][layer]["task"]) for layer in layers]
            plt.plot(xs, base_fps, label="Base-"+str(num_NN))
            plt.plot(xs, task_fps, label="Task-"+str(num_NN))

            # Format plot
            plt.xlabel(more_sharing_label, fontsize=28)
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.ylabel("Throughput (FPS)", fontsize=28)
            plt.ylim(0,20)
            plt.legend(loc=0, fontsize=15)
            plt.title(str(num_NN)+" split NN", fontsize=30)
            plt.tight_layout()
            plt.savefig(plot_dir + "/throughput-"+str(num_NN)+"-NN.pdf")
            plt.clf()

def plot_processor_latency(processors_file, plot_dir):
    layers = preprocess.get_layers(processors_file, 0)
    num_NNs = preprocess.get_num_NNs(processors_file)
    data = get_data(processors_file, "latency-processors")
    width = 0.4
    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            xs = range(len(layers))

            base_fps = [np.average(data[num_NN][layer]["base"]) for layer in layers]
            task_fps = [np.average(data[num_NN][layer]["task"]) for layer in layers]
            base_errs = [np.std(data[num_NN][layer]["base"]) for layer in layers]
            task_errs = [np.std(data[num_NN][layer]["task"]) for layer in layers]

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
            plt.ylim(0, 300)
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
    plot_throughput(csv_file, plot_dir)
    #plot_throughput(csv_file, plot_dir)
    #plot_processor_latency(csv_file, plot_dir)

