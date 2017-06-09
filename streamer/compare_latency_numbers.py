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

            # Hack to make processor specific values
            if experiment_name == "cumulative":
                transformer -= camera
                base -= (transformer + camera)
                task -= (transformer + camera + base)

            data[num_NN][layer]["camera"] = camera
            data[num_NN][layer]["transformer"] = transformer
            data[num_NN][layer]["base"] = base
            data[num_NN][layer]["task"] = task

    return data


def compare(e2e_file, processors_file, queue_file):
    layers = get_layers(processors_file)
    num_NNs = get_num_NNs(processors_file)
    data_e2e = get_data(e2e_file, "cumulative")
    data_processors = get_data(processors_file, "compare")
    data_queue = get_data(queue_file, "compare")

    num_NN = 1
    for num_NN in num_NNs:
        xs = range(len(layers))

        a1 = [data_queue[num_NN][layer]["camera"] for layer in layers]
        a2 = [data_processors[num_NN][layer]["camera"] for layer in layers]
        a3 = [data_e2e[num_NN][layer]["camera"] for layer in layers]

        b1 = [data_queue[num_NN][layer]["transformer"] for layer in layers]
        b2 = [data_processors[num_NN][layer]["transformer"] for layer in layers]
        b3 = [data_e2e[num_NN][layer]["transformer"] for layer in layers]

        c1 = [data_queue[num_NN][layer]["base"] for layer in layers]
        c2 = [data_processors[num_NN][layer]["base"] for layer in layers]
        c3 = [data_e2e[num_NN][layer]["base"] for layer in layers]

        d1 = [data_queue[num_NN][layer]["task"] for layer in layers]
        d2 = [data_processors[num_NN][layer]["task"] for layer in layers]
        d3 = [data_e2e[num_NN][layer]["task"] for layer in layers]

        plot_diffs(a1,a2,a3, layers, "camera", num_NN)
        plot_diffs(b1,b2,b3, layers, "transformer", num_NN)
        plot_diffs(c1,c2,c3, layers, "base", num_NN)
        plot_diffs(d1,d2,d3, layers, "task", num_NN)

def plot_diffs(a, b, c, layers, processor, num_NN):
    diffs = [] 
    for q, p, e2e in zip(a, b, c):
        if e2e == 0:
            diffs.append(0)
        else:
            diffs.append((q + p - e2e) / e2e * 100)
    xs = range(len(diffs))
    plt.clf()
    plt.scatter(xs, diffs)
    plt.xticks(xs, layers, rotation="vertical")
    plt.ylabel("% increase over E2E")
    plt.tight_layout()
    plt.savefig("plots/shared/latency/diffs/"+str(num_NN) + "-" + processor+".pdf")

if __name__ == "__main__":
    e2e_file = sys.argv[1]
    processors_file = sys.argv[2]
    queue_file = sys.argv[3]
    compare(e2e_file, processors_file, queue_file)




