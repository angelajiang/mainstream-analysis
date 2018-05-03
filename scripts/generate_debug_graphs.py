
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

def setups_7hybrid():

    plot_dir = "plots/scheduler/debug/"

    # 043018 budget sweep

    num_apps_list = [2, 4, 6, 8, 10, 15, 20, 25, 30]
    for num_apps in num_apps_list:

        files_by_budget = {}
        files_by_budget_v = {}
        budgets = [100, 150, 200, 250, 300]

        for budget in budgets:

            m1 =  "output/streamer/scheduler/atc/043018/greedy.mainstream.sim.{}.043018-{}.v1".format(budget, num_apps)
            m2 =  "output/streamer/scheduler/atc/043018/stems_cpp.mainstream.sim.{}.043018-{}.v1".format(budget, num_apps)
            m3 =  "output/streamer/scheduler/atc/043018/greedy.nosharing.sim.{}.043018-{}.v1".format(budget, num_apps)
            m4 =  "output/streamer/scheduler/atc/043018/greedy.maxsharing.sim.{}.043018-{}.v1".format(budget, num_apps)
            l1 = "Mainstream-greedy"
            l2 = "Mainstream-stems"
            l3 = "No Sharing"
            l4 = "Max Sharing"
            if num_apps in [2, 4]:
                ms_files = [m1,m2,m3,m4]
                labels = [l1,l2,l3,l4]
                ms_files_v = [m2,m3,m4]
                labels_v = [l2,l3,l4]
            else:
                ms_files = [m1,m3,m4]
                labels = [l1,l3,l4]
                ms_files_v = [m1,m3,m4]
                labels_v = [l1,l3,l4]

            files_by_budget[budget] = {"data": ms_files, "labels": labels}
            files_by_budget_v[budget] = {"data": ms_files_v, "labels": labels_v}

        plot_file ="f1-7hybrid-043018-" + str(num_apps)

        scheduler_comparison.plot_by_budget(files_by_budget, num_apps, plot_file, plot_dir)
        scheduler_comparison.plot_by_budget(files_by_budget_v, num_apps, plot_file, plot_dir, verbose=1)

    # 043018 apps sweep

    for budget in budgets:

        files_by_apps = {}
        files_by_apps_v = {}

        for num_apps in num_apps_list:

            m1 =  "output/streamer/scheduler/atc/043018/greedy.mainstream.sim.{}.043018-{}.v1".format(budget, num_apps)
            m2 =  "output/streamer/scheduler/atc/043018/stems_cpp.mainstream.sim.{}.043018-{}.v1".format(budget, num_apps)
            m3 =  "output/streamer/scheduler/atc/043018/greedy.nosharing.sim.{}.043018-{}.v1".format(budget, num_apps)
            m4 =  "output/streamer/scheduler/atc/043018/greedy.maxsharing.sim.{}.043018-{}.v1".format(budget, num_apps)
            l1 = "Mainstream-greedy"
            l2 = "Mainstream-stems"
            l3 = "No Sharing"
            l4 = "Max Sharing"

            ms_files = [m1,m3,m4]
            labels = [l1,l3,l4]
            files_by_apps[num_apps] = {"data": ms_files, "labels": labels}

        plot_file ="f1-7hybrid-043018-" + str(budget)
        scheduler_comparison.plot_by_num_apps_v1(files_by_apps,
                                                 budget,
                                                 plot_file,
                                                 plot_dir)
        scheduler_comparison.plot_by_num_apps_v1(files_by_apps,
                                                 budget,
                                                 plot_file,
                                                 plot_dir,
                                                 dual=True)


def iii_f1():
    plot_dir = "plots/scheduler/debug/"

    ms1 =  "output/streamer/scheduler/debug/iii-greedy-mainstream-simulator"
    max1 =  "output/streamer/scheduler/debug/iii-greedy-maxsharing-simulator"
    min1 =  "output/streamer/scheduler/debug/iii-greedy-nosharing-simulator"
    ms2  =  "output/streamer/scheduler/debug/iii-stems-mainstream-simulator"
    l1 = "Mainstream Greedy"
    l2 = "Max Sharing"
    l3 = "No Sharing"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    variant_files = [ms2]
    ms_variant_name = "Mainstream DP"
    titles = [t1]

    f_files = ["f1-iii-greedy"]
    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, \
                                        ms_variant_files=variant_files, \
                                        ms_variant_name=ms_variant_name)

    f_files = ["f1-iii-greedy-normalized"]
    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, normalize=True)

def iii_accuracy():

    redcar = "output/mainstream/accuracy/iii/redcar/iii-redcar-accuracy"
    scramble = "output/mainstream/accuracy/iii/scramble/iii-scramble-accuracy"
    bus = "output/mainstream/accuracy/iii/bus/iii-bus-accuracy"
    schoolbus = "output/mainstream/accuracy/iii/schoolbus/iii-schoolbus-accuracy"
    pedestrian = "output/mainstream/accuracy/pedestrian/atrium/atrium-mobilenets-accuracy"
    train = "output/mainstream/accuracy/trains/train-easy/train-easy-mobilenets"
    cars = "output/mainstream/accuracy/cars/cars-stanford-mobilenets-accuracy"
    flowers = "output/mainstream/accuracy/flowers/mobilenets/flowers-40-0.0001"
    cats = "output/mainstream/accuracy/cats/cats-mobilenets-accuracy"

    accuracy_files = [redcar,
                      scramble,
                      bus,
                      schoolbus,
                      pedestrian,
                      train,
                      cars]

    labels = [
              "Red-Car-MobileNets-224",
              "Scramble-MobileNets-224",
              "Bus-MobileNets-224",
              "Schoolbus-MobileNets-224",
              "Pedestrian-MobileNets-224",
              "Train-MobileNets-224",
              "Cars-MobileNets-224"
              ]

    plot_file = "plots/scheduler/debug/7hybrid-mobilenets-accuracy.pdf"
    accuracy_vs_layer.plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

#compare_avg()
setups_7hybrid()
iii_f1()
iii_accuracy()
