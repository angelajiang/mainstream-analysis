
import sys
sys.path.append("scripts/goodness")
import accuracy_vs_layer
sys.path.append("scripts/scheduler")
import scheduler_comparison
import scheduler
from data_util import collect_comb_csvs


################## Maximize F1 Score ##################
plot_dir = "plots/scheduler/exhaustive/"
t1 = ""

def compare_avg():

    m1 =  "output/streamer/scheduler/exhaustive/dp.031318.v0"
    m2 =  "output/streamer/scheduler/exhaustive/exhaustive.031318.v0"
    m3 =  "output/streamer/scheduler/exhaustive/greedy.031318.v0"
    l1 = "DP-hifi"
    l2 = "Exhaustive"
    l3 = "Greedy"
    plot_file ="f1-avg-scheduler-comparison-bar"
    ms_files = [m1,m2,m3]
    labels = [l1,l2,l3]

    scheduler_comparison.plot_bar_v0(ms_files, labels, plot_file, plot_dir)

def setups_9hybrid():
    plot_dir = "plots/scheduler/debug/"

    # greedy
    m1 =  "output/streamer/scheduler/setups/greedy.mainstream.sim.041118.v0"
    m2 =  "output/streamer/scheduler/setups/greedy.maxsharing.sim.041118.v0"
    m3 =  "output/streamer/scheduler/setups/greedy.nosharing.sim.041118.v0"
    l1 = "Mainstream"
    l2 = "Max Sharing"
    l3 = "No Sharing"
    plot_file ="f1-9hybrid-greedy"
    ms_files = [m1,m2,m3]
    labels = [l1,l2,l3]

    scheduler_comparison.plot_by_num_apps_v0(ms_files, labels, 10, plot_file, plot_dir)

def iii_f1():
    plot_dir = "plots/scheduler/debug/"

    ms1 =  "output/streamer/scheduler/debug/iii-greedy-mainstream-simulator"
    max1 =  "output/streamer/scheduler/debug/iii-greedy-maxsharing-simulator"
    min1 =  "output/streamer/scheduler/debug/iii-greedy-nosharing-simulator"
    l1 = "mainstream"
    l2 = "maxsharing"
    l3 = "nosharing"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    titles = [t1]

    f_files = ["f1-iii-greedy"]
    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)

    f_files = ["f1-iii-greedy-normalized"]
    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, normalize=True)

def iii_accuracy():

    redcar = "output/mainstream/accuracy/iii/redcar/iii-redcar-accuracy"
    scramble = "output/mainstream/accuracy/iii/scramble/iii-scramble-accuracy"
    bus = "output/mainstream/accuracy/iii/bus/iii-bus-accuracy"
    schoolbus = "output/mainstream/accuracy/iii/schoolbus/iii-schoolbus-accuracy"

    accuracy_files = [redcar,
                      scramble,
                      bus,
                      schoolbus]

    labels = [
              "Red-Car-MobileNets-224",
              "Scramble-MobileNets-224",
              "Bus-MobileNets-224",
              "Schoolbus-MobileNets-224"
              ]
    plot_file = "plots/accuracy/iii-mobilenets-accuracy.pdf"

    accuracy_vs_layer.plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

#compare_avg()
setups_9hybrid()
iii_f1()
iii_accuracy()
