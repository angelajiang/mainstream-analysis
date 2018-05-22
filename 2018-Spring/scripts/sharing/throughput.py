from dataloaders import Latencies
import plot
from plotutils import agg2series
from plotutils import grids
from plotutils import styles
from utils import save


def inception():
    # TODO: Refactor filename out.
    filename = "../pre-2018-Spring/" + "output/streamer/throughput/" + "inception/flow_control/multi-app"

    num_layers = len(Latencies.layer_idx(filename))
    df = Latencies.as_throughput(Latencies.load(filename))
    df['layer_id_percent'] = (df['layer_id'] / num_layers * 100).astype(int)
    df_view = df[df['layer'] != "dense_2"]

    num_NNs = sorted(set(df['num_NNs'].values))

    # TODO: labels via plotstyles, markers, ...
    # Maybe get_plotstyles(labels=lambda x: x.num_apps + " apps", colors=default, markers=default) 
    grouped = df_view.groupby(['num_NNs', 'layer_id_percent'])
    labels = [str(n) + ' apps' for n in num_NNs]
    series = agg2series(grouped['task_avg'].mean(),
                        names=num_NNs,
                        plotstyles=styles.default(labels=labels))

    plot.variants(series,
                  xgrid=grids.x.frozen_shared,
                  ygrid=lambda *args, **kwargs: grids.y.fps(*args, label="Throughput (FPS)", **kwargs))
    save('sharing', plot_id='task_throughput')


def main():
    inception()


if __name__ == '__main__':
    main()
