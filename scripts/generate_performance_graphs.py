import sys
sys.path.append("scripts")
import layer_sweep

if __name__ == "__main__":
    # Max throughput

    data_file = "/usr0/home/ahjiang/src/private/viscloud/mainstream-analysis/output/streamer/throughput/inception/flow_control/max-benefit"
    plot_file = "/usr0/home/ahjiang/src/private/viscloud/mainstream-analysis/plots/performance/throughput/inception/flow_control/max-throughput.pdf"
    layer_sweep.plot_max_throughput(data_file, plot_file)
