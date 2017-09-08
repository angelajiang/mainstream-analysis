import sys
sys.path.append("scripts")
import num_apps_bar
import layer_sweep
sys.path.append("scripts/scheduler")
import dynamic_scheduler
sys.path.append("scripts/goodness")
import accuracy_vs_layer

if __name__ == "__main__":

    # Max throughput
    data_file = "output/streamer/throughput/inception/flow_control/max-benefit"
    plot_file = "plots/performance/throughput/inception/flow_control/max-throughput.pdf"
    layer_sweep.plot_max_throughput(data_file, plot_file)

    # Latency by split point
    plot_dir = "plots/performance/latency/inception/basic"
    csv_file = "output/streamer/latency/inception/basic/layer_sweep_latency.csv"
    layer_sweep.plot_processor_latency(csv_file, plot_dir)

    # Task throughput by split point
    plot_dir = "plots/performance/throughput/inception/flow_control"
    csv_file = "output/streamer/throughput/inception/flow_control/multi-app"
    layer_sweep.plot_throughput(csv_file, plot_dir)

    # Image level accuracy scheduler
    plot_dir = "plots/scheduler/"
    csv_file = "output/streamer/scheduler/dynamic-uniform.csv" 
    dynamic_scheduler.plot(csv_file, plot_dir)

    # Training accuracy
    accuracy_file1 = "output/mainstream/accuracy/flowers/inception/flowers-40-0.0001-dropout"
    accuracy_file2 = "output/mainstream/accuracy/flowers/resnet/flowers-40-0.0001-chokepoints"
    accuracy_file3 = "output/mainstream/accuracy/flowers/mobilenets/flowers-40-0.0001"
    accuracy_file4 = "output/mainstream/accuracy/paris/resnet/paris-40-0.0001-chokepoints"

    accuracy_files = [accuracy_file1, accuracy_file2, accuracy_file3, accuracy_file4]
    labels = ["Flowers-InceptionV3", "Flowers-ResNet50", "Flowers-Mobilenets-224", "Paris-ResNet50"]
    plot_file = "plots/accuracy/accuracy-by-layer.pdf"

    accuracy_vs_layer.plot_accuracy_vs_layer(accuracy_files, labels, plot_file)

    # Image-level accuracy - Mainstream vs No sharing
    xs, ys = num_apps_bar.get_data("output/streamer/scheduler/dynamic-uniform.csv", 0.015)
    ys2 = [5, 3, 2, 1, 1]
    num_apps_bar.plot("plots/num_apps_bar.pdf", xs, ys, ys2)


