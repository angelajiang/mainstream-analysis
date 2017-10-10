import sys
sys.path.append("scripts")
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
assert mpl.__version__ < '2.0.0'
# mpl.style.use('classic')
import num_apps_bar
import layer_sweep
sys.path.append("scripts/scheduler")
import dynamic_scheduler
import scheduler
sys.path.append("scripts/goodness")
import accuracy_vs_layer
import false_neg_by_stride
import false_neg_by_layer
import false_pos_by_stride
sys.path.append("scripts/accuracy_vs_performance")
import accuracy_tradeoffs
sys.path.append("util")
import layer_latencies
import plot_util
sys.path.append('util/include')
import layers_info
sys.path.append('scripts/deploy')
import visualize
import fairness


import seaborn as sns
sns.set_style("whitegrid")

if __name__ == "__main__":
    mpl.rc('font', **{'sans-serif' : 'Arial',
                      'family' : 'sans-serif'})

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

    fi = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"
    fr = "output/mainstream/accuracy/flowers/resnet/flowers-40-0.0001-chokepoints"
    fm = "output/mainstream/accuracy/flowers/mobilenets/flowers-40-0.0001"
    pr = "output/mainstream/accuracy/paris/resnet/paris-40-0.0001-chokepoints"
    pi = "output/mainstream/accuracy/paris/inception/paris-40-0.0001-dropout"
    pm = "output/mainstream/accuracy/paris/mobilenets/paris-40-0.0001"
    ci = "output/mainstream/accuracy/cats/cats-inception-accuracy"
    cm = "output/mainstream/accuracy/cats/cats-mobilenets-accuracy"
    cr = "output/mainstream/accuracy/cats/cats-resnet-accuracy"

    accuracy_files = [fr, pr, cr, fi, pi, ci, fm, pm, cm]

    labels = [
              "Flowers-ResNet50",
              "Paris-ResNet50",
              "Cats-ResNet50",
              "Flowers-InceptionV3",
              "Paris-InceptionV3",
              "Cats-InceptionV3",
              "Flowers-MobileNets-224",
              "Paris-MobileNets-224",
              "Cats-MobileNets-224",
              ]
    plot_file = "plots/accuracy/accuracy-by-layer.pdf"

    accuracy_vs_layer.plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

    # Accuracy vs throughput
    print "Accuracy vs throughput..."

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

    # Image level accuracy scheduler
    print "Plotting dynamic uniform scheduler..."
    plot_dir = "plots/scheduler/"
    csv_file = "output/streamer/scheduler/dynamic-uniform.csv" 
    dynamic_scheduler.plot(csv_file, plot_dir)


    # Image-level accuracy - Mainstream vs No sharing
    print "Plotting num apps bar..."
    xs, ys = num_apps_bar.get_data("output/streamer/scheduler/dynamic-uniform.csv", 0.015)
    ys2 = [5, 3, 2, 1, 1]
    num_apps_bar.plot("plots/num_apps_bar.pdf", xs, ys, ys2)

    print "Plotting false neg by layer..."
    arch1 = "iv3"
    latency_file1 = "output/streamer/throughput/inception/flow_control/multi-app"
    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"

    plot_dir = "plots/goodness/"

    #plot_false_negative_rate_nosharing(arch1, latency_file1, accuracy_file1, 0.2, 10000, 500, 13, plot_dir, "/tmp/out")
    false_neg_by_layer.plot_false_negative_rate(arch1, latency_file1, accuracy_file1, 0.2, 10000, 250, 14, plot_dir)

    # False neg by stride
    print "Plotting false neg by stride"
    f1 = "../mainstream/log/frame-rate/flowers/synthetic/7"
    f2 = "../mainstream/log/frame-rate/flowers/synthetic/10"
    f3 = "../mainstream/log/frame-rate/flowers/synthetic/14"
    f4 = "../mainstream/log/frame-rate/flowers/synthetic/18"
    f5 = "../mainstream/log/frame-rate/flowers/synthetic/41"
    f6 = "../mainstream/log/frame-rate/flowers/synthetic/64"
    f7 = "../mainstream/log/frame-rate/flowers/synthetic/87"
    f8 = "../mainstream/log/frame-rate/flowers/synthetic/133"
    f9 = "../mainstream/log/frame-rate/flowers/synthetic/165"
    f10 = "../mainstream/log/frame-rate/flowers/synthetic/197"
    f11 = "../mainstream/log/frame-rate/flowers/synthetic/249"
    f12 = "../mainstream/log/frame-rate/flowers/synthetic/280"
    f13 = "../mainstream/log/frame-rate/flowers/synthetic/311"
    plot_file = "plots/frame-rate/frame-rate-flowers-models.pdf"
    '''
    plot_models([f1, f3, f5, f7, f8, f9, f10, f11, f12, f13],
                ["7", "14", "41", "87", "133", "165", "197", "249", "280", "311"],
                plot_file,
                40)
    '''

    f1 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-0"
    f2 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-4"
    f3 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-17"
    f4 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-18"
    f5 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-41"
    f6 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-87"
    f7 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-165"
    f8 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-197"
    f9 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-229"
    f10 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-249"
    f11 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-280"
    f12 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-311"
    f13 = "../mainstream/log/frame-rate/no-afn/train/frame-rate-trains-no-afn-313"
    plot_file = "plots/frame-rate/frame-rate-afn-models.pdf"
    # plot_models([f1, f2, f3, f4, f5, f6, f7, f8, f9, f10, f11, f12, f13],
    #      ["0", "4", "17", "18", "41", "87", "165", "197", "229", "249", "280", "311", "313"], plot_file)

    plot_file = "plots/frame-rate/frame-rate-afn-slo.pdf"
    #plot_slos(f13, plot_file)

    event_lengths = [286, 77, 92, 437, 274, 255, 251, 153]

    plot_file = "plots/frame-rate/frame-rate-afn-dependences.pdf"
    dependent_file = "output/mainstream/frame-rate/no-afn/train/v2/trains-313-dependent-whole"
    independent_file = "output/mainstream/frame-rate/no-afn/train/v2/trains-313-independent-whole"
    empirical_file = "output/mainstream/frame-rate/no-afn/train/v2/trains-313-empirical-temporal"
    files = [dependent_file, independent_file, empirical_file]
    labels = ["Dependent", "Independent", "Empirical"]
    false_neg_by_stride.plot_dependence(files, labels, event_lengths, plot_file)

    plot_file = "plots/frame-rate/frame-rate-afn-dependences-with-correlation.pdf"
    dependent_file = "output/mainstream/frame-rate/no-afn/train/v2/trains-313-dependent-whole"
    independent_file = "output/mainstream/frame-rate/no-afn/train/v2/trains-313-independent-whole"
    empirical_file = "output/mainstream/frame-rate/no-afn/train/v2/trains-313-empirical-temporal"
    correlation_file = "output/mainstream/frame-rate/no-afn/train/v2/trains-313-correlation"
    files = [dependent_file, independent_file, empirical_file, correlation_file]
    labels = ["Dependent", "Independent", "Empirical", "Correlation"]
    false_neg_by_stride.plot_dependence(files, labels, event_lengths, plot_file)


    # False positive frequency
    print "Plotting false positive frequency..."
    plot_file = "plots/goodness/vid4"
    false_pos_by_stride.plot_fpf_by_stride(15, 0.028,  0.0011, 0.015, 0.00056, 1.3, 7, plot_file)

    # Scheduler

    plot_dir = "plots/scheduler"

    ## Event length param sweep
    print "Plotting scheduler graphs..."
    ms1 = "output/streamer/scheduler/scheduler-s0-100-ms.csv" 
    max1 = "output/streamer/scheduler/scheduler-s0-100-max.csv" 
    min1 = "output/streamer/scheduler/scheduler-s0-100-min.csv" 
    f1 ="scheduler-s0-100"
    t1 = "Within 100ms (1.4 Frames)"

    #ms2 = "output/streamer/scheduler/scheduler-s0-500-ms.csv" 
    ms2= "output/streamer/scheduler/correlation/scheduler-correlation-mainstream-c0-ll0" 
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

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

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

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

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

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

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

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ## Independence versus dependence

    ms1 = "output/streamer/scheduler/scheduler-s0-500-dependence-mainstream" 
    max1 = "output/streamer/scheduler/scheduler-s0-500-dependence-maxsharing" 
    min1 = "output/streamer/scheduler/scheduler-s0-500-dependence-nosharing" 
    f1 ="scheduler-s0-500-flowers-dependent"
    t1 = "Correlation = 1"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    #ms2 = "output/streamer/scheduler/scheduler-s0-500-ms.csv" 
    ms2= "output/streamer/scheduler/correlation/scheduler-correlation-mainstream-c0-ll0" 
    max2 = "output/streamer/scheduler/scheduler-s0-500-max.csv" 
    min2 = "output/streamer/scheduler/scheduler-s0-500-min.csv" 
    f2 ="scheduler-s0-500-flowers-independent"
    t2 = "Correlation = 0"

    ms_files = [ms2]
    max_files = [max2]
    min_files = [min2]
    f_files = [f2]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t2]

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    ## Multiple applications
    ms1 = "output/streamer/scheduler/correlation/scheduler-correlation-mainstream-c0.1664-ll0" 
    max1 = "output/streamer/scheduler/correlation/scheduler-correlation-maxsharing-c0.1664" 
    min1 = "output/streamer/scheduler/correlation/scheduler-correlation-nosharing-c0.1664" 
    f1 ="scheduler-s0-500-c0.1664"
    t1 = "Correlation = 0.17"
    plot_dir = "plots/scheduler"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

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

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)

    # FNR
    ms1 = "output/streamer/scheduler/correlation/scheduler-correlation-mainstream-c0.1664-ll0" 
    max1 = "output/streamer/scheduler/correlation/scheduler-correlation-maxsharing-c0.1664" 
    min1 = "output/streamer/scheduler/correlation/scheduler-correlation-nosharing-c0.1664" 
    f1 ="scheduler-false-neg-rate"
    t1 = ""
    plot_dir = "plots/scheduler"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    scheduler.plot_fnr(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_fnr(ms_files, max_files, min_files, f_files_annotated, titles, plot_dir, True)



    print "Plot layer latencies..."
    # Layer latencies
    csv_file = "output/streamer/latency/inception/basic/latency-by-layer.csv"
    layer_names = layers_info.InceptionV3_Layer_Names
    plot_dir = "plots/performance/latency/inception/basic/"
    layer_latencies.print_and_plot_latencies(csv_file, layer_names, "InceptionV3", plot_dir)

    csv_file = "output/streamer/latency/mobilenets/basic/latency-by-layer.csv"
    layer_names = layers_info.MobileNets_Layer_Names
    plot_dir = "plots/performance/latency/mobilenets/basic/"
    layer_latencies.print_and_plot_latencies(csv_file, layer_names, "MobileNets-224", plot_dir)

    csv_file = "output/streamer/latency/resnet/basic/latency-by-layer.csv"
    layer_names = layers_info.ResNet50_Layer_Names
    plot_dir = "plots/performance/latency/resnet/basic/"
    layer_latencies.print_and_plot_latencies(csv_file, layer_names, "ResNet-50", plot_dir)

    print "Plot deploy time series..."
    # Data created by mainstream analyze_deployment
    # Format: frame_id, is_analyzed
    f0 = "output/streamer/deploy/train/train2-10apps-nosharing"
    f1 = "output/streamer/deploy/train/train2-10apps-mainstream"
    f2 = "output/streamer/deploy/train/train2-10apps-maxsharing"
    thumbnail = "output/train-example.jpg"
    plot_dir = "plots/deploy"
    files = [f0, f1]
    objs = [plot_util.NO_SHARING, plot_util.MAINSTREAM]
    visualize.visualize_deployment(files, objs, plot_dir, thumbnail)

    print "Plot app fairness..."
    prefix = "output/streamer/scheduler/combinations"

    f1 = "scheduler-apps-fairness"
    t1 = ""
    plot_dir = "plots/scheduler"

    f_files = [f1]
    titles = [t1]

    fairness.plot(prefix, f_files, titles, plot_dir)
