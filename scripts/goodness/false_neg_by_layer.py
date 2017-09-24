# -*- coding: utf-8 -*-
import pprint as pp
import math
import sys
import matplotlib
import numpy as np
import random
from itertools import cycle
import matplotlib.pyplot as plt

sys.path.append('include/')
import layers_info
sys.path.append('scripts/util/')
import preprocess

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def get_throughput_data(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            op_full = vals[0]
            layer = preprocess.op_to_layer(op_full)
            num_NN = int(vals[1])
            base = float(vals[2])
            tasks = [float(t) for t in vals[3:]]
            task = np.average(tasks)

            if num_NN not in data.keys():
                data[num_NN] = {}
            if layer not in data[num_NN].keys():
                data[num_NN][layer] = {}

            if (task == 0):
                task = base

            data[num_NN][layer]["base"] = base
            data[num_NN][layer]["task"] = task
    return data

def get_accuracy_data(architecture, csv_file):
    if architecture == "iv3":
        layer_name_by_num_frozen = layers_info.InceptionV3_Layer_Names
    elif architecture == "r50":
        layer_name_by_num_frozen = layers_info.ResNet50_Layer_Names
    elif architecture == "mnets":
        layer_name_by_num_frozen = layers_info.MobileNets_Layer_Names

    acc_by_layer = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            frozen_index = int(vals[0])
            acc = float(vals[1])
            layer = layer_name_by_num_frozen[frozen_index]
            acc_by_layer[layer] = acc
    return acc_by_layer, layer_name_by_num_frozen

def get_probability_miss(p_identified_list, min_event_length_ms, max_fps, observed_fps):
    stride = max_fps / float(observed_fps)
    d = min_event_length_ms / float(1000) * max_fps
    p_misses = []
    for p_identified in p_identified_list:
        if d < 1:
            print "Event of length", min_event_length_ms, "ms cannot be detected at", max_fps, "FPS"
            p_miss = 1
        elif d < stride:
            p_encountered = d / stride
            p_hit = p_encountered * p_identified
            p_miss = 1 - p_hit
        else:
            mod = (d % stride)
            p1 = (d - (mod)) / d
            r1 = math.floor(d / stride)
            p2 = mod / d
            r2 = math.ceil(d / stride)
            p_not_identified = 1 - p_identified
            p_miss = p1 * math.pow(p_not_identified, r1) + \
                        p2 * math.pow(p_not_identified, r2)
        p_misses.append(p_miss)
    return np.average(p_misses)

def plot_false_negative_rate_nosharing(arch, latency_file, accuracy_file, sigma, num_events,\
                                       min_event_length_ms, max_fps, plot_dir, outfile):
    num_NNs = preprocess.get_num_NNs(latency_file)
    marker = "h"
    layer = preprocess.get_layers(latency_file, 0)[0]
    throughput_data = get_throughput_data(latency_file)
    acc_data, layer_name_by_num_frozen = get_accuracy_data(arch, accuracy_file)

    for i in range(2): # Hack to get dimensions to match between 1st and 2nd graph
        xs = []
        ys = []
        for num_NN in num_NNs:

            xs.append(num_NN)

            throughput = throughput_data[num_NN][layer]["task"]
            accuracy  = acc_data[layer]
            acc_dist = [random.gauss(accuracy, sigma) for i in range(num_events)]

            p_miss = get_probability_miss(acc_dist, min_event_length_ms, max_fps, throughput)
            ys.append(p_miss)

        plt.scatter(xs, ys, s=50, marker=marker, edgecolor='black', label=str(num_NN)+" apps")

        plt.xlabel(u"More sharing →\n(inc fps, dec acc)", fontsize=28)
        plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
        plt.tick_params(axis='y', which='major', labelsize=24)
        plt.tick_params(axis='y', which='minor', labelsize=20)
        plt.ylabel("False negative rate", fontsize=28)

        #plt.title("Sigma = " + str(sigma), fontsize=30)
        plt.legend(loc=0, fontsize=15)
        plt.tight_layout()

        plt.savefig(plot_dir +"/no-sharing-fnr-" + str(num_NN) + "apps-" + \
                                str(min_event_length_ms) + "ms-" + \
                                str(sigma) + "sig.pdf")
        plt.clf()

    with open(outfile, "w+") as f:
        for x, y in zip(xs, ys):
            line = str(x) + "," + str(round(y,4)) + "\n"
            f.write(line)

def plot_false_negative_rate(arch, latency_file, accuracy_file, sigma, num_events, min_event_length_ms, max_fps, plot_dir):
    num_NNs = preprocess.get_num_NNs(latency_file)
    shapes = ["o", "h", "D", "x", "1", "*", "P", "8"]
    for i in range(2): # Hack to get dimensions to match between 1st and 2nd graph
        for num_NN in [4]:
            cycol = cycle('crmkbgy').next
            #for num_NN, marker in zip(num_NNs[3:7], shapes):
            marker = "h"
            layers = preprocess.get_layers(latency_file, 0)

            throughput_data = get_throughput_data(latency_file)
            acc_data, layer_name_by_num_frozen = get_accuracy_data(arch, accuracy_file)

            xs  = range(0, len(layers))
            throughputs  = [throughput_data[num_NN][layer]["task"] for layer in layers]
            all_accuracies  = [acc_data[layer] for layer in layers]
            # If there is only one app, no matter what layer, accuracy is at its max
            if num_NN == 1:
                accuracies = [max(all_accuracies) for layer in layers]
            else:
                accuracies  = [acc_data[layer] for layer in layers]


            ys = []
            num_frozen_list = []
            fpses = []
            for fps, acc, layer in zip(throughputs, accuracies, layers):
                acc_dist = [random.gauss(acc, sigma) for i in range(num_events)]
                p_miss = get_probability_miss(acc_dist, min_event_length_ms, max_fps, fps)
                ys.append(p_miss)

                # Get info for annotation
                for num_frozen, layer_name in layer_name_by_num_frozen.iteritems():
                    if layer ==  layer_name:
                        break
                num_frozen_list.append(num_frozen)
                fpses.append(fps)

            plt.scatter(xs, ys, s=50, marker=marker, color=cycol(), edgecolor='black', label=str(num_NN)+" apps")

            # Annotate optimal point
            min_y = min(ys)
            x, num_frozen, fps = \
                    [(x, num_frozen, round(fps,0)) for x, y, num_frozen, fps \
                                                        in zip(xs,ys, num_frozen_list, fpses) if y==min_y][0]

            max_layers = max(layer_name_by_num_frozen.keys()) + 1
            percent_frozen = int(num_frozen / float(max_layers) * 100)

            plt.annotate("Best: Share "+str(percent_frozen) +"% layers @ " + str(fps) + " FPS",
                         xy=(x, min_y),
                         xytext=(-300, 170),
                         xycoords='data',
                         fontsize=22,
                         textcoords='offset points',
                         arrowprops=dict(arrowstyle="->"))

            plt.xlabel(u"More sharing →\n(inc fps, dec acc)", fontsize=28)
            plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
            plt.tick_params(axis='y', which='major', labelsize=24)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.xlim(6, len(layers))
            plt.ylim(0, 0.2)
            plt.ylabel("False negative rate", fontsize=28)

            #plt.title("Sigma = " + str(sigma), fontsize=30)
            plt.gca().yaxis.grid(True)
            plt.legend(loc=0, fontsize=20)
            plt.tight_layout()

            plt.savefig(plot_dir +"/false-neg-" + str(num_NN) + "apps-" + \
                                    str(min_event_length_ms) + "ms-" + \
                                    str(sigma) + "sig-" + \
                                    str(max_fps) + "fps.pdf")
            plt.clf()

if __name__ == "__main__":

    arch1 = "iv3"
    latency_file1 = "output/streamer/throughput/inception/flow_control/multi-app"
    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"

    plot_dir = "plots/goodness/"

    #plot_false_negative_rate_nosharing(arch1, latency_file1, accuracy_file1, 0.2, 10000, 500, 13, plot_dir, "/tmp/out")
    plot_false_negative_rate(arch1, latency_file1, accuracy_file1, 0.2, 10000, 250, 14, plot_dir)

