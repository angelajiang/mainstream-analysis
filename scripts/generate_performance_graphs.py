import sys
sys.path.append("scripts")
import num_apps_bar
import layer_sweep
sys.path.append("scripts/scheduler")
import dynamic_scheduler
import scheduler
sys.path.append("scripts/goodness")
import accuracy_vs_layer
sys.path.append("scripts/accuracy_vs_performance")
import accuracy_tradeoffs

import seaborn as sns

sns.set()

if __name__ == "__main__":

    # Max throughput
    print "Plotting max throughput..."
    data_file = "output/streamer/throughput/inception/flow_control/max-benefit"
    plot_file = "plots/performance/throughput/inception/flow_control/max-throughput.pdf"
    layer_sweep.plot_max_throughput(data_file, plot_file)

    # Latency by split point
    print "Plotting latency by split point..."
    plot_dir = "plots/performance/latency/inception/basic"
    csv_file = "output/streamer/latency/inception/basic/layer_sweep_latency.csv"
    layer_sweep.plot_processor_latency(csv_file, plot_dir)

    # Task throughput by split point
    print "Plotting throughput by split point..."
    plot_dir = "plots/performance/throughput/inception/flow_control"
    csv_file = "output/streamer/throughput/inception/flow_control/multi-app"
    layer_sweep.plot_throughput(csv_file, plot_dir)

    # Training accuracy
    print "Plotting training accuracy..."
    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"
    accuracy_file2 = "output/mainstream/accuracy/flowers/resnet/flowers-40-0.0001-chokepoints"
    accuracy_file3 = "output/mainstream/accuracy/flowers/mobilenets/flowers-40-0.0001"
    accuracy_file4 = "output/mainstream/accuracy/paris/resnet/paris-40-0.0001-chokepoints"
    accuracy_file5 = "output/mainstream/accuracy/paris/inception/paris-40-0.0001-dropout"
    accuracy_file6 = "output/mainstream/accuracy/paris/mobilenets/paris-40-0.0001"
    accuracy_file7 = "output/mainstream/accuracy/cats/cats-inception-accuracy"

    accuracy_files = [
                      accuracy_file2,
                      accuracy_file5,
                      accuracy_file4,
                      accuracy_file1,
                      #accuracy_file7,
                      accuracy_file6,
                      accuracy_file3
                      ]

    labels = [
              "Flowers-ResNet50",
              "Paris-InceptionV3",
              "Paris-ResNet50",
              "Flowers-InceptionV3",
              #"Cats-InceptionV3",
              "Paris-MobileNets-224",
              "Flowers-MobileNets-224"
              ]
    plot_file = "plots/accuracy/accuracy-by-layer.pdf"
    accuracy_vs_layer.plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

    # Image level accuracy scheduler
    print "Plotting dynamic uniform scheduler..."
    plot_dir = "plots/scheduler/"
    csv_file = "output/streamer/scheduler/dynamic-uniform.csv" 
    dynamic_scheduler.plot(csv_file, plot_dir)

    accuracy_vs_layer.plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

    # Image-level accuracy - Mainstream vs No sharing
    print "Plotting num apps bar..."
    xs, ys = num_apps_bar.get_data("output/streamer/scheduler/dynamic-uniform.csv", 0.015)
    ys2 = [5, 3, 2, 1, 1]
    num_apps_bar.plot("plots/num_apps_bar.pdf", xs, ys, ys2)

    # Scheduler

    plot_dir = "plots/scheduler"

    ## Event length param sweep
    print "Plotting scheduler graphs..."
    ms1 = "output/streamer/scheduler/scheduler-s0-100-ms.csv" 
    max1 = "output/streamer/scheduler/scheduler-s0-100-max.csv" 
    min1 = "output/streamer/scheduler/scheduler-s0-100-min.csv" 
    f1 ="scheduler-s0-100"
    t1 = "Within 100ms (1.4 Frames)"

    ms2 = "output/streamer/scheduler/scheduler-s0-500-ms.csv" 
    max2 = "output/streamer/scheduler/scheduler-s0-500-max.csv" 
    min2 = "output/streamer/scheduler/scheduler-s0-500-min.csv" 
    f2 ="scheduler-s0-500"
    t2 = "Within 500ms (7 Frames)"

    ms3 = "output/streamer/scheduler/scheduler-s0-250-mainstream" 
    max3 = "output/streamer/scheduler/scheduler-s0-250ms-independent-maxsharing" 
    min3 = "output/streamer/scheduler/scheduler-s0-250-nosharing" 
    f3 ="scheduler-s0-250"
    t3 = "Within 250ms (2.8 Frames)"

    ms_files = [ms1, ms2, ms3]
    max_files = [max1, max2, max3]
    min_files = [min1, min2, min3]
    f_files = [f1, f2, f3]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1, t2, t3]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ## Different applications
    ms1 = "output/streamer/scheduler/scheduler-s0-250-mainstream" 
    max1 = "output/streamer/scheduler/scheduler-s0-250ms-independent-maxsharing" 
    min1 = "output/streamer/scheduler/scheduler-s0-250-nosharing" 
    f1 ="scheduler-s0-250-flowers"
    t1 = "Flowers"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ms2 = "output/streamer/scheduler/scheduler-s0-250-paris-mainstream" 
    max2 = "output/streamer/scheduler/scheduler-s0-250-paris-maxsharing" 
    min2 = "output/streamer/scheduler/scheduler-s0-250-paris-nosharing" 
    f2 ="scheduler-s0-250-paris"
    t2 = "Paris"

    ms_files = [ms2]
    max_files = [max2]
    min_files = [min2]
    f_files = [f2]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t2]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ms3 = "output/streamer/scheduler/scheduler-s0-250-cats-mainstream" 
    max3 = "output/streamer/scheduler/scheduler-s0-250-cats-maxsharing" 
    min3 = "output/streamer/scheduler/scheduler-s0-250-cats-nosharing" 
    f3 ="scheduler-s0-250-cats"
    t3 = "Cats"

    ms_files = [ms1, ms2, ms3]
    max_files = [max1, max2, max3]
    min_files = [min1, min2, min3]
    f_files = [f1, f2, f3]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1, t2, t3]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ## Independence versus dependence
    ms1 = "output/streamer/scheduler/scheduler-s0-250-dependence-mainstream" 
    max1 = "output/streamer/scheduler/scheduler-s0-250-dependence-maxsharing" 
    min1 = "output/streamer/scheduler/scheduler-s0-250-dependence-nosharing" 
    f1 ="scheduler-s0-250-flowers-dependent"
    t1 = "Dependent accuracy"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ms2 = "output/streamer/scheduler/scheduler-s0-250-mainstream" 
    max2 = "output/streamer/scheduler/scheduler-s0-250ms-independent-maxsharing" 
    min2 = "output/streamer/scheduler/scheduler-s0-250-nosharing" 
    f2 ="scheduler-s0-250-flowers-independent"
    t2 = "Independent accuracy"

    ms_files = [ms2]
    max_files = [max2]
    min_files = [min2]
    f_files = [f2]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t2]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ms1 = "output/streamer/scheduler/scheduler-s0-500-dependence-mainstream" 
    max1 = "output/streamer/scheduler/scheduler-s0-500-dependence-maxsharing" 
    min1 = "output/streamer/scheduler/scheduler-s0-500-dependence-nosharing" 
    f1 ="scheduler-s0-500-flowers-dependent"
    t1 = "Dependent accuracy"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ms2 = "output/streamer/scheduler/scheduler-s0-500-ms.csv" 
    max2 = "output/streamer/scheduler/scheduler-s0-500-max.csv" 
    min2 = "output/streamer/scheduler/scheduler-s0-500-min.csv" 
    f2 ="scheduler-s0-500-flowers-independent"
    t2 = "Independent accuracy"

    ms_files = [ms2]
    max_files = [max2]
    min_files = [min2]
    f_files = [f2]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t2]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ## Multiple applications
    ms1 = "output/streamer/scheduler/cost/scheduler-s0-250-multiapp-mainstream" 
    max1 = "output/streamer/scheduler/cost/scheduler-s0-250-multiapp-maxsharing" 
    min1 = "output/streamer/scheduler/cost/scheduler-s0-250-multiapp-nosharing" 
    f1 ="scheduler-s0-250-flowers-multiapp"
    t1 = "Multiple applications"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    scheduler.plot(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    # Accuracy vs throughput

    arch1 = "iv3"
    arch2 = "r50"
    arch3 = "mnets"

    latency_file1 = "output/streamer/latency/inception/basic/latency-processors-iv3.csv"
    latency_file2 = "output/streamer/latency/resnet/basic/latency-processors-r50.csv"
    latency_file3 = "output/streamer/latency/mobilenets/basic/latency.csv"

    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"
    accuracy_file2 = "output/mainstream/accuracy/flowers/resnet/flowers-40-0.0001-chokepoints"
    accuracy_file3 = "output/mainstream/accuracy/flowers/mobilenets/flowers-40-0.0001"

    arches = [arch1, arch2, arch3]
    latency_files = [latency_file1, latency_file2, latency_file3]
    accuracy_files = [accuracy_file1, accuracy_file2, accuracy_file3]
    labels = ["InceptionV3", "ResNet50", "MobileNets-224"]

    plot_dir = "plots/tradeoffs/flowers"

    accuracy_tradeoffs.plot_accuracy_vs_fps(arches, latency_files, accuracy_files, labels, plot_dir)

