import dataloaders
import plot
from plotutils import ex, comb, agg2series
from plotutils import grids
from plotutils import legends
from utils import save


def _get_data(exp_id, metric, selected_x):
    workspace_dir = "../pre-2018-Spring/" + "output/streamer/scheduler/atc/{}".format(metric)
    rows = []
    for x_votes in selected_x:
        schedules = dataloaders.load_schedules(exp_id,
                                               "{metric}-{dataset}-500-x{x}-mainstream-simulator".format(metric=metric, dataset=exp_id, x=x_votes),
                                               workspace=workspace_dir)
        rows += ex(schedules,
                   each=lambda s: {'num_apps': s.num_apps, 'f1': s.extra('f1_est')},
                   constant={'scheduler': 'greedy',
                             'x_voting': str(x_votes) + '-voting',
                             'metric': metric,
                             'sharing': 'mainstream'})
    df = comb(rows)
    return df


def x_voting(dataset, opt_metric, plot_metric, selected_x):
    df = _get_data(dataset, opt_metric, selected_x)

    grouped = df.groupby(['x_voting', 'num_apps'])
    series = agg2series(grouped[plot_metric].mean(),
                        names=[str(x) + '-voting' for x in selected_x],
                        plotstyles=None,
                        plotparams='fg')
    series.append(plot.frontier(series, voting_train_f1_hack=dataset == 'train'))
    ax = plot.variants(series,
                       legend=legends.reversed,
                       xgrid=grids.x.num_apps,
                       ygrid=grids.y.get(plot_metric))

    save('scheduler', 'x_voting', '{}-{}-{}-frontier'.format(dataset, opt_metric, plot_metric))


def main():
    x_voting("pedestrian", "f1", "f1", [1, 3, 5, 7])
    x_voting("train", "f1", "f1", [1, 3, 5, 7])


if __name__ == '__main__':
    main()
