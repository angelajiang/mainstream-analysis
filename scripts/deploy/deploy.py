
import pprint as pp
import sys
import matplotlib
import numpy as np

sys.path.append("scripts/util")
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()
import seaborn as sns
sns.set_style("whitegrid")


def get_data(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            scheduler = vals[0]
            num_apps = int(vals[1])
            fnr = 1 - float(vals[2])

            if scheduler not in data.keys():
                data[scheduler] = {"xs":[], "ys":[]}
            data[scheduler]["xs"].append(num_apps)
            data[scheduler]["ys"].append(fnr)
    return data

def plot(csv_file, plot_file):
    data = get_data(csv_file)
    schedulers = ["nosharing", "maxsharing", "mainstream"]
    for scheduler, scheduler_data in data.iteritems():
        if scheduler == "mainstream":
            plot_config = plot_util.MAINSTREAM
        elif scheduler == "nosharing":
            plot_config = plot_util.NO_SHARING
        elif scheduler == "maxsharing":
            plot_config = plot_util.MAX_SHARING

        plt.plot(scheduler_data["xs"], scheduler_data["ys"], linewidth=2,
                 label=plot_config["label"],
                 color=plot_config["color"],
                 zorder=3,
                 marker = plot_config["marker"])

        plt.legend(loc=0, fontsize=20)
        plt.tick_params(axis='y', which='major', labelsize=28)
        plt.tick_params(axis='y', which='minor', labelsize=20)
        #plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
        plt.xlabel("Number of applications", fontsize=35)
        plt.ylabel("False negative rate", fontsize=35)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.grid()
    plt.savefig(plot_file)
    plt.clf()

if __name__ == "__main__":
    csv_file = "output/streamer/deploy/daisy/results-perturbed-d6e98b20"
    plot_file = "plots/deploy/deploy-perturbed.pdf"
    plot(csv_file, plot_file)

    csv_file = "output/streamer/deploy/daisy/results-independent-97081724"
    plot_file = "plots/deploy/deploy-independent.pdf"
    plot(csv_file, plot_file)

    csv_file = "output/streamer/deploy/daisy/results"
    plot_file = "plots/deploy/deploy-dependent.pdf"
    plot(csv_file, plot_file)
