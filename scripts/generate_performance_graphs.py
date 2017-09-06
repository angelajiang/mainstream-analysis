import sys
sys.path.append("scripts")
import layer_sweep

if __name__ == "__main__":
    # Max throughput

    data_file = "output/streamer/throughput/inception/flow_control/max-benefit"
    plot_file = "plots/performance/throughput/inception/flow_control/max-throughput.pdf"
    layer_sweep.plot_max_throughput(data_file, plot_file)

    plot_dir = "plots/performance/latency/inception/basic"
    csv_file = "output/streamer/latency/inception/basic/layer_sweep_latency.csv"
    layer_sweep.plot_throughput(csv_file, plot_dir)
    layer_sweep.plot_processor_latency(csv_file, plot_dir)
