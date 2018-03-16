
import sys
sys.path.append("scripts/scheduler")
import scheduler_comparison
from data_util import collect_comb_csvs


################## Maximize F1 Score ##################
plot_dir = "plots/scheduler/comparison/"
t1 = ""

def compare_avg():

    m1 =  "output/streamer/scheduler/comparison/avg/dp.031318.v0"
    m2 =  "output/streamer/scheduler/comparison/avg/exhaustive.031318.v0"
    m3 =  "output/streamer/scheduler/comparison/avg/greedy.031318.v0"
    l1 = "DP-hifi"
    l2 = "Exhaustive"
    l3 = "Greedy"
    ms_files = [m1,m2,m3]
    labels = [l1,l2,l3]

    plot_file ="f1-avg-scheduler-comparison-bar-031318"
    scheduler_comparison.plot_bar_v0(ms_files, labels, plot_file, plot_dir)

    plot_file ="f1-avg-scheduler-comparison-numapps-031318"
    scheduler_comparison.plot_by_num_apps_v0(ms_files, labels, 50, plot_file, plot_dir)

    m1 =  "output/streamer/scheduler/comparison/avg/dp.031418.v0"
    m2 =  "output/streamer/scheduler/comparison/avg/exhaustive.031418.v0"
    m3 =  "output/streamer/scheduler/comparison/avg/greedy.031418.v0"
    l1 = "Dynamic Programming"
    l2 = "Exhaustive"
    l3 = "Greedy"
    ms_files = [m1,m2,m3]
    labels = [l1,l2,l3]

    plot_file ="f1-avg-scheduler-comparison-bar-031418"
    scheduler_comparison.plot_bar_v0(ms_files, labels, plot_file, plot_dir)

    plot_file ="f1-avg-scheduler-comparison-numapps-031418"
    scheduler_comparison.plot_by_num_apps_v0(ms_files, labels, 200, plot_file, plot_dir)

def compare_latency():

    m1 =  "output/streamer/scheduler/comparison/performance/dp.performance.v0"
    m2 =  "output/streamer/scheduler/comparison/performance/exhaustive.performance.v0"
    m3 =  "output/streamer/scheduler/comparison/performance/greedy.performance.v0"
    l1 = "Dynamic Programming"
    l2 = "Exhaustive"
    l3 = "Greedy"
    ms_files = [m1,m2,m3]
    labels = [l1,l2,l3]

    plot_file ="f1-latency-scheduler-comparison-performance"
    scheduler_comparison.plot_latency_v0(ms_files, labels, plot_file, plot_dir)

compare_avg()
compare_latency()
