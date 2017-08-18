import pprint as pp
import sys
import matplotlib
import numpy as np

sys.path.append('scripts/util/')
import preprocess

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

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

MARKERS = ["o", "h", "D", "x", "1", "*", "p", "8"]

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
    layers = get_layers(csv_file)
    num_NNs = preprocess.get_num_NNs(csv_file)
    data = get_data(csv_file, "throughput")
    labels = ["No sharing", "Max sharing"]

    for layer, label in zip(layers, labels):
        task_fps = [np.average(data[num_NN][layer]["task"]) for num_NN in num_NNs]
        plt.plot(num_NNs, task_fps, label=label, lw=2)

    # Format plot
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.xlabel("Number of applications", fontsize=28)
    plt.ylabel("Throughput (FPS)", fontsize=28)
    plt.ylim(0,20)
    plt.legend(loc=0, fontsize=15)
    plt.tight_layout()
    plt.savefig(plot_file)
    print plot_file
    plt.clf()

def plot_throughput(csv_file, plot_dir):
    layers = [preprocess.op_to_layer(l) for l in LAYERS]
    num_NNs = preprocess.get_num_NNs(csv_file)
    data = get_data(csv_file, "throughput")

    xs = range(len(layers))

    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN, marker in zip(num_NNs, MARKERS):

            task_fps = [np.average(data[num_NN][layer]["task"]) for layer in layers]
            plt.plot(xs, task_fps, marker=marker, label=str(num_NN)+" apps", lw=2)

        # Format plot
        plt.xlabel("More sharing ->", fontsize=28)
        plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
        plt.ylabel("Throughput (FPS)", fontsize=28)

        plt.tick_params(axis='y', which='major', labelsize=28)
        plt.tick_params(axis='y', which='minor', labelsize=20)
        plt.ylim(0,20)

        plt.legend(loc=0, fontsize=15)
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
            plt.xlabel("More sharing ->", fontsize=28)
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
    layers = get_layers(processors_file)
    num_NNs = preprocess.get_num_NNs(processors_file)
    data = get_data(processors_file, "latency-processors")
    width = 0.4
    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            xs = range(len(layers))

            base_fps = [np.average(data[num_NN][layer]["base"]) for layer in layers]
            task_fps = [np.average(data[num_NN][layer]["task"]) for layer in layers]
            plt.bar(xs, base_fps, width, color = "seagreen", label="Base NNE")
            plt.bar(xs, task_fps, width, bottom=base_fps, color = "dodgerblue", label="Task NNE")

            plt.xlabel("More sharing ->", fontsize=28)
            plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
            plt.ylim(0,400)
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.legend(loc=0, fontsize=15, ncol=2)
            plt.ylabel("Processor Latency (ms)", fontsize=20)
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

