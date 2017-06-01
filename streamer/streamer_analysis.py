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

def plot_simultaneous(csv_file):
    xs = []
    ys = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            fps = float(vals[1])
            xs.append(num_apps)
            ys.append(fps)
    width = 0.5
    plt.bar(xs, ys, width=width, color="lightcoral")
    plt.xticks(xs, xs, ha='center')
    plt.tick_params(axis='both', which='major', labelsize=28)
    plt.tick_params(axis='both', which='minor', labelsize=20)
    plt.xlabel("Number of simultaneous NNs", fontsize=28)
    plt.ylabel("Throughput (FPS)", fontsize=28)
    plt.title("Simultaneous full NNs", fontsize=30)
    plt.tight_layout()
    plt.savefig("plots/simultaneous.pdf")

def plot_partial(csv_file):
    labels = []
    ys = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
            fps = float(vals[1])
            labels.append(layer)
            ys.append(fps)
    xs = range(len(ys))
    width = 0.5
    plt.bar(xs, ys, width=width, color="lightcoral")
    ind = np.arange(len(labels))
    plt.xticks(ind + width / 2, labels, rotation="vertical")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.ylabel("Throughput (FPS)", fontsize=28)
    plt.title("Single partial NN", fontsize=30)
    plt.tight_layout()
    plt.savefig("plots/partial.pdf")


def plot_shared(csv_file):
    layers = []
    num_apps = []
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
            num_app = int(vals[1])
            base = float(vals[2])
            task = float(vals[3])
            if num_app not in data.keys():
                data[num_app] = {}
            data[num_app][layer] = {}
            data[num_app][layer]["base"] = base
            data[num_app][layer]["task"] = task
            if layer not in layers:
                layers.append(layer)
            if num_app not in num_apps:
                num_apps.append(num_app)

    for num_app in num_apps:
        base_fps = [data[num_app][layer]["base"] for layer in layers]
        xs = range(len(layers))
        plt.plot(xs, base_fps, label=str(num_app) + " apps")
    plt.xticks(xs, layers, rotation="vertical")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.ylabel("Base NN Throughput (FPS)", fontsize=28)
    plt.legend(loc=0, fontsize=15)
    plt.tight_layout()
    plt.savefig("plots/shared/base.pdf")
    plt.clf()

    for num_app in num_apps:
        task_fps = [data[num_app][layer]["task"] for layer in layers]
        xs = range(len(layers))
        plt.plot(xs, task_fps, label=str(num_app) + " apps")
    plt.xticks(xs, layers, rotation="vertical")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.yscale("log")
    plt.ylabel("Avg Task NN FPS", fontsize=28)
    plt.legend(loc=0, fontsize=15)
    plt.tight_layout()
    plt.savefig("plots/shared/task.pdf")
    plt.clf()

    for num_app in num_apps:
        base_fps = [data[num_app][layer]["base"] for layer in layers]
        task_fps = [data[num_app][layer]["task"] for layer in layers]
        all_fps = zip(base_fps, task_fps)
        bottleneck_fps = [min(pair_fps) for pair_fps in all_fps]
        xs = range(len(layers))
        plt.plot(xs, bottleneck_fps, label=str(num_app) + " apps")
    plt.xticks(xs, layers, rotation="vertical")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.ylabel("Bottleneck NN FPS", fontsize=28)
    plt.legend(loc=0, fontsize=15)
    plt.tight_layout()
    plt.savefig("plots/shared/bottleneck.pdf")
    plt.clf()

    for num_app in num_apps:
        base_fps = [data[num_app][layer]["base"] for layer in layers]
        task_fps = [data[num_app][layer]["task"] for layer in layers]
        xs = range(len(layers))
        plt.plot(xs, base_fps, label="Base-"+str(num_app))
        plt.plot(xs, task_fps, label="Task-"+str(num_app))
        plt.xticks(xs, layers, rotation="vertical")
        plt.tick_params(axis='y', which='major', labelsize=28)
        plt.tick_params(axis='y', which='minor', labelsize=20)
        plt.ylabel("Throughput (FPS)", fontsize=28)
        plt.legend(loc=0, fontsize=15)
        plt.title(str(num_app)+" split NN", fontsize=30)
        plt.yscale("log")
        plt.ylim(0, 1500)
        plt.tight_layout()
        plt.savefig("plots/shared/"+str(num_app)+"-NN.pdf")

if __name__ == "__main__":
    cmd = sys.argv[1]
    csv_file = sys.argv[2]
    if cmd == "simultaneous":
        plot_simultaneous(csv_file)
    elif cmd == "partial":
        plot_partial(csv_file)
    elif cmd == "shared":
        plot_shared(csv_file)
    else:
        print "cmd must be in {simultaneous, partial, shared}"

