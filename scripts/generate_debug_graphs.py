
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

    # 041118 greedy
    m1 =  "output/streamer/scheduler/setups/greedy.mainstream.sim.041118.v0"
    m2 =  "output/streamer/scheduler/setups/greedy.maxsharing.sim.041118.v0"
    m3 =  "output/streamer/scheduler/setups/greedy.nosharing.sim.041118.v0"
    m4 =  "output/streamer/scheduler/setups/stems.mainstream.sim.041118.v0"
    l1 = "Mainstream"
    l2 = "Max Sharing"
    l3 = "No Sharing"
    l4 = "Mainstream DP"
    plot_file ="f1-9hybrid-greedy"
    ms_files = [m1,m2,m3, m4]
    labels = [l1,l2,l3,l4]

    scheduler_comparison.plot_by_num_apps_v0(ms_files, labels, 10, plot_file, plot_dir)

    # 041718 4 apps

    num_apps = 4

    files_by_budget = {}
    files_by_budget_v = {}
    budgets = [100, 150, 200, 250, 300]

    for budget in budgets:

        m1 =  "output/streamer/scheduler/osdi/041718/greedy.mainstream.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
        m2 =  "output/streamer/scheduler/osdi/041718/stems_cpp.mainstream.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
        m3 =  "output/streamer/scheduler/osdi/041718/greedy.nosharing.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
        m4 =  "output/streamer/scheduler/osdi/041718/greedy.maxsharing.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
        m5 =  "output/streamer/scheduler/osdi/041718/exhaustive.mainstream.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
        l1 = "Mainstream-greedy"
        l2 = "Mainstream-stems"
        l3 = "No Sharing"
        l4 = "Max Sharing"
        l5 = "Mainstream-exhaustive"
        ms_files = [m1,m2,m3,m4,m5]
        labels = [l1,l2,l3,l4,l5]
        files_by_budget[budget] = {"data": ms_files, "labels": labels}

        ms_files = [m1,m3,m4]
        labels = [l1,l3,l4]
        files_by_budget_v[budget] = {"data": ms_files, "labels": labels}

    plot_file ="f1-9hybrid-041718-" + str(num_apps)
    scheduler_comparison.plot_by_budget(files_by_budget, num_apps, plot_file, plot_dir)
    scheduler_comparison.plot_by_budget(files_by_budget_v, num_apps, plot_file, plot_dir, verbose=1)

    # 041718 apps sweep

    num_apps_list = [5, 15, 20, 25, 30]
    for num_apps in num_apps_list:

        files_by_budget = {}
        files_by_budget_v = {}
        budgets = [100, 150, 200, 250, 300]

        for budget in budgets:

            m1 =  "output/streamer/scheduler/osdi/041718/greedy.mainstream.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
            m2 =  "output/streamer/scheduler/osdi/041718/stems_cpp.mainstream.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
            m3 =  "output/streamer/scheduler/osdi/041718/greedy.nosharing.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
            m4 =  "output/streamer/scheduler/osdi/041718/greedy.maxsharing.sim.041718-"+str(budget) + "-" + str(num_apps) + ".v0"
            l1 = "Mainstream-greedy"
            l2 = "Mainstream-stems"
            l3 = "No Sharing"
            l4 = "Max Sharing"
            ms_files = [m1,m2,m3,m4]
            labels = [l1,l2,l3,l4]
            ms_files = [m1,m3,m4]
            labels = [l1,l3,l4]
            files_by_budget[budget] = {"data": ms_files, "labels": labels}

            ms_files = [m1,m3,m4]
            labels = [l1,l3,l4]
            files_by_budget_v[budget] = {"data": ms_files, "labels": labels}

        plot_file ="f1-9hybrid-041718-" + str(num_apps)

        scheduler_comparison.plot_by_budget(files_by_budget, num_apps, plot_file, plot_dir, version="v0")
        scheduler_comparison.plot_by_budget(files_by_budget_v, num_apps, plot_file, plot_dir, verbose=1, version="v0")

    # 042518

    num_apps_list = [4, 10]
    for num_apps in num_apps_list:

        version = "v1"
        m1 =  "output/streamer/scheduler/atc/042518/greedy.mainstream.sim.042518-"+str(num_apps)+"."+version
        m2 =  "output/streamer/scheduler/atc/042518/greedy.nosharing.sim.042518-"+str(num_apps) +"."+version
        m3 =  "output/streamer/scheduler/atc/042518/greedy.maxsharing.sim.042518-"+str(num_apps)+"."+version
        m4 =  "output/streamer/scheduler/atc/042518/stems_cpp.mainstream.sim.042518-"+str(num_apps)+"."+version
        l1 = "Mainstream-greedy"
        l2 = "No Sharing"
        l3 = "Max Sharing"
        l4 = "Stems CPP"

        ms_files = [m1,m2,m3]
        labels = [l1,l2,l3]
        data =  {"data": ms_files, "labels": labels}
        data_v =  {"data": ms_files, "labels": labels}

        plot_file ="f1-9hybrid-042518-" + str(num_apps)

        if num_apps == 4:
            ms_files = [m1,m2,m3,m4]
            labels = [l1,l2,l3,l4]
            data =  {"data": ms_files, "labels": labels}

            ms_files = [m2,m3,m4]
            labels = [l2,l3,l4]
            data_v = {"data": ms_files, "labels": labels}

        scheduler_comparison.plot_by_budget(data, num_apps, plot_file, plot_dir, version=version)
        scheduler_comparison.plot_by_budget(data_v, num_apps, plot_file, plot_dir, verbose=1, version=version)

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

    redcar0 = "output/mainstream/accuracy/iii/redcar/iii-redcar-accuracy-small"
    redcar1 = "output/mainstream/accuracy/iii/redcar/iii-redcar-accuracy"
    scramble = "output/mainstream/accuracy/iii/scramble/iii-scramble-accuracy"
    bus = "output/mainstream/accuracy/iii/bus/iii-bus-accuracy"
    schoolbus = "output/mainstream/accuracy/iii/schoolbus/iii-schoolbus-accuracy"

    accuracy_files = [redcar0,
                      redcar1,
                      scramble,
                      bus,
                      schoolbus]

    labels = [
              "Red-Car-MobileNets-224",
              "Red-Car-Better-MobileNets-224",
              "Scramble-MobileNets-224",
              "Bus-MobileNets-224",
              "Schoolbus-MobileNets-224"
              ]
    plot_file = "plots/scheduler/debug/iii-mobilenets-accuracy.pdf"

    accuracy_vs_layer.plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

#compare_avg()
setups_9hybrid()
iii_f1()
iii_accuracy()
