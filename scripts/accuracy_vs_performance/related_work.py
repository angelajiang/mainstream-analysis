import pprint as pp
import sys
import matplotlib
import numpy as np

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()


def get_data(csv_file):
    speeds = {"pascal":{}, "ti1080":{}, "maxwell":{}}
    accuracies = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            dnn = vals[0]
            top1_error = float(vals[1])
            pascal = float(vals[2])
            ti1080 = float(vals[3])
            maxwell = float(vals[4])
            accuracies[dnn] = (1 - (top1_error / 100))
            speeds["pascal"][dnn] = pascal
            speeds["ti1080"][dnn] = ti1080
            speeds["maxwell"][dnn] = maxwell
    return speeds, accuracies

def plot_johnson_tradeoffs(data_file, plot_dir):
    speeds, accuracies = get_data(data_file)
    for i in range(2):              # Hack to get dimensions to match between 1st and 2nd graph
        for gpu in speeds.keys():
            xs = []
            ys = []
            labels = []
            for dnn in accuracies.keys():
                if speeds[gpu][dnn] != -1:
                    xs.append(speeds[gpu][dnn])
                    ys.append(accuracies[dnn])
                    labels.append(dnn)

            plt.scatter(xs, ys, s=50, color="darkorchid", edgecolor='black', linewidth='0.5')

            plt.tick_params(axis='y', which='major', labelsize=28)
            plt.tick_params(axis='y', which='minor', labelsize=20)
            plt.tick_params(axis='x', which='major', labelsize=28)
            plt.tick_params(axis='x', which='minor', labelsize=20)

            for label, x, y in zip(labels, xs, ys):
                plt.annotate(
                    label,
                    xy=(x, y), xytext=(60, 20),
                    textcoords='offset points', ha='right', va='bottom')
            plt.legend(loc=0, fontsize=15, ncol=2)
            plt.xlim(0,180)

            plt.xlabel("Latency (ms)", fontsize=20)
            plt.ylabel("Top-1 Accuracy", fontsize=20)
            plt.title(gpu, fontsize=30)
            plt.tight_layout()
            plt.savefig(plot_dir +"/johnson-tradeoffs-" + gpu + ".pdf")
            plt.clf()


if __name__ == "__main__":
    johnson_file = sys.argv[1]
    plot_dir = sys.argv[2]
    plot_johnson_tradeoffs(johnson_file, plot_dir)

