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
            num_NNs = int(vals[0])
            fps = float(vals[1])
            xs.append(num_NNs)
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

def plot_throughput(csv_file):
    layers = []
    num_NNs = []
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
            # Hack to simulate pass-through processor
            if (base == 0):
                base = transformer
            if (task == 0):
                task = base
            if num_NN not in data.keys():
                data[num_NN] = {}
            data[num_NN][layer] = {}
            data[num_NN][layer]["camera"] = camera
            data[num_NN][layer]["transformer"] = transformer
            data[num_NN][layer]["base"] = base
            data[num_NN][layer]["task"] = task
            if layer not in layers:
                layers.append(layer)
            if num_NN not in num_NNs:
                num_NNs.append(num_NN)

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

def plot_latency_breakdown(e2e_file, processors_file, queue_file):
    layers = []
    num_NNs = []
    data_e2e = {}
    data_processors = {}
    data_queue = {}
    with open(e2e_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
            num_NN = int(vals[1])
            camera = float(vals[2])
            transformer = float(vals[3])
            base = float(vals[4])
            task = float(vals[5])
            if num_NN not in data_e2e.keys():
                data_e2e[num_NN] = {}
            data_e2e[num_NN][layer] = {}
            data_e2e[num_NN][layer]["camera"] = camera
            data_e2e[num_NN][layer]["transformer"] = transformer
            data_e2e[num_NN][layer]["base"] = base
            data_e2e[num_NN][layer]["task"] = task

    with open(processors_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
            num_NN = int(vals[1])
            camera = float(vals[2])
            transformer = float(vals[3])
            base = float(vals[4])
            task = float(vals[5])
            if num_NN not in data_processors.keys():
                data_processors[num_NN] = {}
            data_processors[num_NN][layer] = {}
            data_processors[num_NN][layer]["camera"] = camera
            data_processors[num_NN][layer]["transformer"] = transformer
            data_processors[num_NN][layer]["base"] = base
            data_processors[num_NN][layer]["task"] = task
            if layer not in layers:
                layers.append(layer)
            if num_NN not in num_NNs:
                num_NNs.append(num_NN)

    with open(queue_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = op_to_layer(op_full)
            num_NN = int(vals[1])
            camera = float(vals[2])
            transformer = float(vals[3])
            base = float(vals[4])
            task = float(vals[5])
            if num_NN not in data_queue.keys():
                data_queue[num_NN] = {}
            data_queue[num_NN][layer] = {}
            data_queue[num_NN][layer]["camera"] = camera
            data_queue[num_NN][layer]["transformer"] = transformer
            data_queue[num_NN][layer]["base"] = base
            data_queue[num_NN][layer]["task"] = task

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
            g = [data_queue[num_NN][layer]["task"] for layer in layers]
            h = [data_processors[num_NN][layer]["task"] for layer in layers]
            e = [data_e2e[num_NN][layer]["camera"] for layer in layers]
            f = [data_e2e[num_NN][layer]["transformer"] for layer in layers]
            g = [data_e2e[num_NN][layer]["task"] for layer in layers]
            h = [data_e2e[num_NN][layer]["task"] for layer in layers]

            b1 = [a[j] for j in range(len(a))]
            b2 = [a[j] +b[j] for j in range(len(a))]
            b3 = [a[j] +b[j] + c[j] for j in range(len(a))]
            b4 = [a[j] +b[j] + c[j] + d[j] for j in range(len(a))]
            b5 = [a[j] +b[j] + c[j] + d[j] + e[j] for j in range(len(a))]
            b6 = [a[j] +b[j] + c[j] + d[j] + e[j] +f[j] for j in range(len(a))]
            b7 = [a[j] +b[j] + c[j] + d[j] + e[j] +f[j] + g[j] for j in range(len(a))]

            b8 = [e[j] for j in range(len(a))]
            b9 = [e[j] +f[j] for j in range(len(a))]
            b10 = [e[j]+f[j] + g[j] for j in range(len(a))]

            plt.bar(xs, a, width, color = "lightseagreen", label="Camera-Q")
            plt.bar(xs, b, width, bottom=b1, color = "seagreen", label="Camera-P")
            plt.bar(xs, c, width, bottom=b2, color = "deepskyblue", label="Transfomer-Q")
            plt.bar(xs, d, width, bottom=b3, color = "dodgerblue", label="Transfomer-P")
            plt.bar(xs, e, width, bottom=b4, color = "mediumpurple", label="Base-Q-"+str(num_NN))
            plt.bar(xs, f, width, bottom=b5, color = "darkorchid", label="Base-P-"+str(num_NN))
            plt.bar(xs, g, width, bottom=b6,color = "lightpink", label="Task-Q-"+str(num_NN))
            plt.bar(xs, h, width, bottom=b7,color = "palevioletred", label="Task-P-"+str(num_NN))
            plt.bar(xs, e, width, color = "slategrey", label="Camera-E2E-"+str(num_NN))
            plt.bar(xs, f, width, color = "slategrey", bottom=b8, label="Transformer-E2E-"+str(num_NN))
            plt.bar(xs, g, width, color = "slategrey", bottom=b9, label="Base-E2E-"+str(num_NN))
            plt.bar(xs, h, width, color = "slategrey", bottom=b10, label="Task-E2E-"+str(num_NN))

            plt.ylim(0,1500)
            plt.xticks(xs, layers, rotation="vertical")
            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.legend(loc=0, fontsize=15, ncol=2)
            plt.ylabel("Latency breakdown (ms)", fontsize=28)
            plt.title(str(num_NN) + " NNs", fontsize=30)
            plt.tight_layout()
            plt.savefig("plots/shared/latency/breakdown-"+str(num_NN)+"-NN.pdf")
            plt.clf()

def plot_e2e_latency(csv_file):
    layers = []
    num_NNs = []
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
            data[num_NN][layer] = {}
            data[num_NN][layer]["camera"] = camera
            data[num_NN][layer]["transformer"] = transformer
            data[num_NN][layer]["base"] = base
            data[num_NN][layer]["task"] = task
            if layer not in layers:
                layers.append(layer)
            if num_NN not in num_NNs:
                num_NNs.append(num_NN)

    width = 0.4
    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in num_NNs:
            xs = range(len(layers))

            base_fps = [data[num_NN][layer]["base"] for layer in layers]
            task_fps = [data[num_NN][layer]["task"] for layer in layers]
            camera_fps = [data[num_NN][layer]["camera"] for layer in layers]
            transformer_fps = [data[num_NN][layer]["transformer"] for layer in layers]

            plt.bar(xs, camera_fps, width, color = "mediumturquoise", label="Camera")
            plt.bar(xs, transformer_fps, width, bottom=camera_fps, color = "dodgerblue", label="Transfomer")
            plt.bar(xs, base_fps, width, bottom=transformer_fps, color = "lightcoral", label="Base-"+str(num_NN))
            plt.bar(xs, task_fps, width, bottom=base_fps,color = "orchid", label="Task-"+str(num_NN))

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
    if cmd == "simultaneous":
        plot_simultaneous(csv_file)
    elif cmd == "partial":
        plot_partial(csv_file)
    elif cmd == "throughput":
        plot_throughput(csv_file)
    elif cmd == "latency-e2e":
        plot_e2e_latency(csv_file)
    elif cmd == "latency-breakdown":
        processors_file = sys.argv[3]
        queue_file = sys.argv[4]
        plot_latency_breakdown(csv_file, processors_file, queue_file)
    else:
        print "cmd must be in {simultaneous, partial, throughput, latency-e2e, latency-breakdown}"

