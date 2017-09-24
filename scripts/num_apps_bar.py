
import pprint as pp
import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt
# matplotlib.style.use('classic')

sys.path.append("scripts/util")
import plot_util

'''
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()
'''

def get_data(csv_file, acc_loss_thresh):
# For each  fps_slo, get max num_apps with rel_acc_loss < acc_loss_thresh
    data_by_fps = {} # by fps_slo
    xs = []
    ys = []
    fps_slos = [2, 4, 6, 8, 10]
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            num_apps = int(vals[0])
            fps_slo = float(vals[1])
            if fps_slo not in fps_slos:
                continue
            rel_acc_loss = float(vals[2])
            if fps_slo not in data_by_fps.keys():
                data_by_fps[fps_slo] = {"num_apps": [], "acc_losses": []}
            data_by_fps[fps_slo]["num_apps"].append(num_apps)
            data_by_fps[fps_slo]["acc_losses"].append(rel_acc_loss)
    for fps_slo, data in sorted(data_by_fps.iteritems()):
        max_napps = \
            max([napps for napps, loss in zip(data["num_apps"], data["acc_losses"]) \
                        if loss <= acc_loss_thresh])
        xs.append(fps_slo)
        ys.append(max_napps)
    return xs, ys

def plot(plot_file, slos, ys_mainstream, ys_nosharing):

    n_groups = len(slos)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.2

    rects1 = ax.bar(index, ys_nosharing, bar_width,
                    color=plot_util.NO_SHARING["color"],
                    hatch=plot_util.NO_SHARING["pattern"],
                    label=plot_util.NO_SHARING["label"])
    rects2 = ax.bar(index + (bar_width), ys_mainstream, bar_width,
                    color=plot_util.MAINSTREAM['color'],
                    hatch=plot_util.MAINSTREAM["pattern"],
                    label=plot_util.MAINSTREAM["label"])

    #ax.set_xticks((ind + bar_width * 2) / 2)
    xs = [i + (bar_width * (3 / 2)) for i in np.arange(len(slos))]
    ax.set_xticks(xs)
    labels = ["{:g} ms".format(round((1. / slo) * 1000.)) for slo in slos]
    # labels = map("{} FPS".format, slos)
    ax.set_xticklabels(labels)
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.tick_params(axis='both', which='minor', labelsize=20)
    ax.tick_params(axis='y', which='major', labelsize=25)
    ax.tick_params(axis='y', which='minor', labelsize=20)
    # plt.xlabel("Throughput", fontsize=28)
    plt.xlabel("Inter-frame time", fontsize=28)
    plt.ylabel('Number of concurrent apps', fontsize=30)
    plt.title('W/in 99% relative accuracy', fontsize=30)
    plt.legend(loc=0, fontsize=25)
    plt.gca().yaxis.grid(True)
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.clf()

if __name__ == "__main__":
    xs, ys = get_data("output/streamer/scheduler/dynamic-uniform.csv", 0.02)
    ys2 = [5, 3, 2, 1, 1]
    plot("plots/num_apps_bar.pdf", xs, ys, ys2)
