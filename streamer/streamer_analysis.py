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

def get_layers(csv_file):
    layers = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
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

def get_data(csv_file, experiment_name):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
            num_NN = int(vals[1])
            camera = float(vals[2])
            transformer = float(vals[3])
            base = float(vals[4])
            task = float(vals[5])
            if num_NN not in data.keys():
                data[num_NN] = {}
            if layer not in data[num_NN].keys():
                data[num_NN][layer] = {}

            # Hack to simulate pass-through processor
            if experiment_name == "throughput":
                if (base == 0):
                    base = transformer
                if (task == 0):
                    task = base

            data[num_NN][layer]["camera"] = camera
            data[num_NN][layer]["transformer"] = transformer
            data[num_NN][layer]["base"] = base
            data[num_NN][layer]["task"] = task
    return data

def plot_throughput(csv_file):
    layers = get_layers(csv_file)
    num_NNs = get_num_NNs(csv_file)
    data = get_data(csv_file, "throughput")

    for num_NN in num_NNs:
        base_fps = [data[num_NN][layer]["base"] for layer in layers]
        xs = range(len(layers))
        plt.plot(xs, base_fps, label=str(num_NN) + " NNs")
    plt.xticks(xs, layers, rotation="vertical")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.ylabel("Base NN Throughput (FPS)", fontsize=28)
    plt.ylim(0, 32)
    plt.legend(loc=0, fontsize=15)
    plt.tight_layout()
    plt.savefig("plots/shared/throughput/base.pdf")
    plt.clf()

    for num_NN in num_NNs:
        task_fps = [data[num_NN][layer]["task"] for layer in layers]
        xs = range(len(layers))
        plt.plot(xs, task_fps, label=str(num_NN) + " NNs")
    plt.xticks(xs, layers, rotation="vertical")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.ylabel("Avg Task NN FPS", fontsize=28)
    plt.ylim(0, 32)
    plt.legend(loc=0, fontsize=15)
    plt.tight_layout()
    plt.savefig("plots/shared/throughput/task.pdf")
    plt.clf()

    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            xs = range(len(layers))

            base_fps = [data[num_NN][layer]["base"] for layer in layers]
            task_fps = [data[num_NN][layer]["task"] for layer in layers]
            camera_fps = [data[num_NN][layer]["camera"] for layer in layers]
            transformer_fps = [data[num_NN][layer]["transformer"] for layer in layers]
            plt.plot(xs, base_fps, label="Base-"+str(num_NN))
            plt.plot(xs, task_fps, label="Task-"+str(num_NN))
            plt.plot(xs, camera_fps, label="Camera")
            plt.plot(xs, transformer_fps, label="Transfomer")

            # Format plot
            plt.xticks(xs, layers, rotation="vertical")
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.ylabel("Throughput (FPS)", fontsize=28)
            plt.ylim(0, 32)
            plt.legend(loc=0, fontsize=15)
            plt.title(str(num_NN)+" split NN", fontsize=30)
            plt.tight_layout()
            plt.savefig("plots/shared/throughput/throughput-"+str(num_NN)+"-NN.pdf")
            plt.clf()

def plot_latency_breakdown(processors_file, queue_file):
    layers = get_layers(processors_file)
    num_NNs = get_num_NNs(processors_file)
    data_processors = get_data(processors_file, "latency-e2e")
    data_queue = get_data(queue_file, "latency-breakdown")

    width = 0.4
    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            xs = range(len(layers))

            a = [data_queue[num_NN][layer]["camera"] for layer in layers]
            b = [data_processors[num_NN][layer]["camera"] for layer in layers]
            c = [data_queue[num_NN][layer]["transformer"] for layer in layers]
            d = [data_processors[num_NN][layer]["transformer"] for layer in layers]
            e = [data_queue[num_NN][layer]["base"] for layer in layers]
            f = [data_processors[num_NN][layer]["base"] for layer in layers]
            g  = [data_queue[num_NN][layer]["task"] for layer in layers]
            h  = [data_processors[num_NN][layer]["task"] for layer in layers]

            b1 = [a[j] for j in range(len(a))]
            b2 = [a[j] +b[j] for j in range(len(a))]
            b3 = [a[j] +b[j] + c[j] for j in range(len(a))]
            b4 = [a[j] +b[j] + c[j] + d[j] for j in range(len(a))]
            b5 = [a[j] +b[j] + c[j] + d[j] + e[j] for j in range(len(a))]
            b6 = [a[j] +b[j] + c[j] + d[j] + e[j] +f[j] for j in range(len(a))]
            b7 = [a[j] +b[j] + c[j] + d[j] + e[j] +f[j] + g[j] for j in range(len(a))]

            plt.bar(xs, a, width, color = "lightseagreen", label="Camera-Q")
            plt.bar(xs, b, width, bottom=b1, color = "seagreen", label="Camera-P")
            plt.bar(xs, c, width, bottom=b2, color = "deepskyblue", label="Transfomer-Q")
            plt.bar(xs, d, width, bottom=b3, color = "dodgerblue", label="Transfomer-P")
            plt.bar(xs, e, width, bottom=b4, color = "mediumpurple", label="Base-Q-"+str(num_NN))
            plt.bar(xs, f, width, bottom=b5, color = "darkorchid", label="Base-P-"+str(num_NN))
            plt.bar(xs, g, width, bottom=b6,color = "lightpink", label="Task-Q-"+str(num_NN))
            plt.bar(xs, h, width, bottom=b7,color = "palevioletred", label="Task-P-"+str(num_NN))

            plt.ylim(0,1500)
            plt.xticks(xs, layers, rotation="vertical")
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.legend(loc=0, fontsize=15, ncol=2)
            plt.ylabel("Queue + Processor Latency (ms)", fontsize=20)
            plt.title(str(num_NN) + " NNs", fontsize=30)
            plt.tight_layout()
            plt.savefig("plots/shared/latency/breakdown-"+str(num_NN)+"-NN.pdf")
            plt.clf()

def plot_e2e_latency(csv_file):
    layers = get_layers(csv_file)
    num_NNs = get_num_NNs(csv_file)
    data = get_data(csv_file, "latency-e2e")

    width = 0.4
    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            xs = range(len(layers))

            base_fps = [data[num_NN][layer]["base"] for layer in layers]
            task_fps = [data[num_NN][layer]["task"] for layer in layers]
            camera_fps = [data[num_NN][layer]["camera"] for layer in layers]
            transformer_fps = [data[num_NN][layer]["transformer"] for layer in layers]

            plt.bar(xs, camera_fps, width, color = "seagreen", label="Camera")
            plt.bar(xs, transformer_fps, width, bottom=camera_fps, color = "dodgerblue", label="Transfomer")
            plt.bar(xs, base_fps, width, bottom=transformer_fps, color = "darkorchid", label="Base-"+str(num_NN))
            plt.bar(xs, task_fps, width, bottom=base_fps,color = "palevioletred", label="Task-"+str(num_NN))

            plt.ylim(0,1500)
            plt.xticks(xs, layers, rotation="vertical")
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.legend(loc=0, fontsize=15)
            plt.ylabel("E2E Latency (ms)", fontsize=28)
            plt.title(str(num_NN) + " NNs", fontsize=30)
            plt.tight_layout()
            plt.savefig("plots/shared/latency/e2e-"+str(num_NN)+"-NN.pdf")
            plt.clf()

if __name__ == "__main__":
    cmd = sys.argv[1]
    csv_file = sys.argv[2]
    if cmd == "throughput":
        plot_throughput(csv_file)
    elif cmd == "latency-e2e":
        plot_e2e_latency(csv_file)
    elif cmd == "latency-breakdown":
        queue_file = sys.argv[3]
        plot_latency_breakdown(csv_file, queue_file)
    else:
        print "cmd must be in {throughput, latency-e2e, latency-breakdown}"

