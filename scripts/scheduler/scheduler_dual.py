import matplotlib
import sys
sys.path.append("scripts")
import scheduler

sys.path.append("scripts/util")
import plot_util

matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()

def plot_f1_dual(ms_files, max_files, min_files, plot_files, titles, plot_dir, annotated=False):
    fig, ax1 = plt.subplots()
    ax2 = ax1.twinx()

    for i in range(2):
        for ms_file, max_file, min_file, plot_file, title \
                in zip(ms_files, max_files, min_files, plot_files, titles):

            xs1, ys1, errs1, losses1, fpses1 = scheduler.get_f1_data(ms_file)
            xs2, ys2, errs2, losses2, fpses2 = scheduler.get_f1_data(max_file)
            xs3, ys3, errs3, losses3, fpses3 = scheduler.get_f1_data(min_file)

            ax2.plot(xs3, fpses3, lw=2, markersize=8, alpha=0.2,
                     marker=plot_util.NO_SHARING['marker'],
                     color=plot_util.NO_SHARING['color'])
            ax2.plot(xs2, fpses2, lw=2, markersize=8, alpha=0.2,
                     marker=plot_util.MAX_SHARING['marker'],
                     color=plot_util.MAX_SHARING['color'])
            ax2.plot(xs1, fpses1, lw=2, markersize=8, alpha=0.2,
                     marker=plot_util.MAINSTREAM['marker'],
                     color=plot_util.MAINSTREAM['color'])

            l1 = ax1.plot(xs3, ys3, lw=4, markersize=8,
                         marker=plot_util.NO_SHARING['marker'],
                         color=plot_util.NO_SHARING['color'],
                         label=plot_util.NO_SHARING['label'])
            l2 = ax1.plot(xs2, ys2, lw=4, markersize=8,
                         marker=plot_util.MAX_SHARING['marker'],
                         color=plot_util.MAX_SHARING['color'],
                         label=plot_util.MAX_SHARING['label'])
            l3 = ax1.plot(xs1, ys1, lw=4, markersize=8,
                         marker=plot_util.MAINSTREAM['marker'],
                         color=plot_util.MAINSTREAM['color'],
                         label=plot_util.MAINSTREAM['label'])

            ax1.tick_params(axis='y', which='major', labelsize=23)
            ax1.tick_params(axis='y', which='minor', labelsize=20)
            ax1.tick_params(axis='x', which='major', labelsize=23)
            ax1.tick_params(axis='x', which='minor', labelsize=20)

            ax2.tick_params(axis='y', which='major', labelsize=23)
            ax2.tick_params(axis='y', which='minor', labelsize=20)
            ax2.tick_params(axis='x', which='major', labelsize=23)
            ax2.tick_params(axis='x', which='minor', labelsize=20)

            ax1.set_xlim(max(min(xs1),2), max(xs1))
            ax1.set_ylim(0, 1)

            lns = l1+l2+l3
            labels = [l.get_label() for l in lns]
            ax1.legend(lns, labels, loc=0, fontsize=15)

            ax1.set_xlabel("Number of concurrent apps", fontsize=30)
            ax1.set_ylabel("Event F1-score", fontsize=30)
            ax2.set_ylabel("Average FPS", fontsize=30)
            plt.tight_layout()
            plt.gca().xaxis.grid(True)
            plt.gca().yaxis.grid(True)

            plt.savefig(plot_dir + "/" + plot_file + "-f1-dual.pdf")


if __name__ == "__main__":

    ################ F1-score ##################

    plot_dir = "plots/scheduler/atc/maximize-f1"
    t1 = ""

    ms1 =  "output/streamer/scheduler/atc/f1/f1-pedestrian-500-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-pedestrian-500-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-pedestrian-500-nosharing"
    f1 ="f1-pedestrian-500"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
