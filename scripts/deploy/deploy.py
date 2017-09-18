
import pprint as pp
import sys
import matplotlib
import numpy as np

sys.path.append("scripts/util")
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()


def get_data(csv_file):
    data = {}
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            video_name = vals[0]
            dependence = vals[1]
            num_apps = int(vals[2])
            scheduler = vals[3]
            fnr = 1 - float(vals[4])

            if dependence not in data.keys():
                data[dependence] = {}
            if scheduler not in data[dependence].keys():
                data[dependence][scheduler] = {"xs":[], "ys":[]}
            data[dependence][scheduler]["xs"].append(num_apps)
            data[dependence][scheduler]["ys"].append(fnr)
    return data

def plot(csv_file, plot_dir):
    data = get_data(csv_file)
    schedulers = ["No", "Max", "MS"]
    for dependence, plot_data in data.iteritems():
        for scheduler in schedulers:
            scheduler_data = plot_data[scheduler]
            if scheduler == "MS":
                plot_config = plot_util.MAINSTREAM
                label = "Mainstream"
            elif scheduler == "No":
                plot_config = plot_util.NO_SHARING
                label = "No sharing"
            elif scheduler == "Max":
                plot_config = plot_util.MAX_SHARING
                label = "Max sharing"

            plt.plot(scheduler_data["xs"], scheduler_data["ys"], linewidth=2,
                     label=label,
                     zorder=3,
                     marker = plot_config["marker"])

        plt.legend(loc=0, fontsize=20)
        plt.tick_params(axis='y', which='major', labelsize=28)
        plt.tick_params(axis='y', which='minor', labelsize=20)
        plt.tick_params(axis='x', which='both', bottom='off', top='off', labelbottom='off')
        plt.xlabel("Number of applications", fontsize=35)
        plt.ylabel("False negative rate", fontsize=35)
        plt.ylim(0, 1)
        plt.tight_layout()
        plt.grid()
        plot_file = plot_dir + "/deploy-" + dependence + ".pdf"
        plt.savefig(plot_file)
        plt.clf()

if __name__ == "__main__":
    csv_file = "output/streamer/deploy/daisy"
    plot_dir = "plots/deploy"
    plot(csv_file, plot_dir)
