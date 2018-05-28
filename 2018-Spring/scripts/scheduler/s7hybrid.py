# Usage: python -m scripts.scheduler.7hybrid
import dataloaders
import plot
from plotutils import ex, comb, agg2series
from plotutils import legends
from plotutils import styles
from plotutils import grids
from plotutils import Annotation, add_annotations
from utils import save, memoize
import matplotlib.pyplot as plt


@memoize()
def _get_data(exp_id, series_names):
    setups = dataloaders.load_setups(exp_id,
                                     setup_file_str="/setups.{exp_id}-*{version}.pickle",
                                     legacy='InconsistentIds')

    rows = []
    for series_name in series_names:
        schedules = dataloaders.load_schedules("050318", "greedy." + series_name + ".sim.*.v1",
                                               variant='v1+metrics',
                                               setups=setups)
        # Extract some attributes from the schedules.
        # Add on some based on the file name.
        rows += ex(schedules,
                   constant={'scheduler': 'greedy', 'sharing': series_name})
    df = comb(rows)
    return df


def metric_7hybrid(metrics=['f1']):
    exp_id = "050318"
    series_names = ["mainstream", "maxsharing", "nosharing"]

    df = _get_data(exp_id, series_names)

    # See Pandas: Group By: split-apply-combine
    # https://pandas.pydata.org/pandas-docs/stable/groupby.html

    for budget in set(df['budget'].values):
        df_view = df[df['budget'] == budget]
        # Group <setups> by number of apps, aggregate by mean.
        grouped = df_view.groupby(['sharing', 'num_apps'])

        series2 = agg2series(grouped['fps'].mean(),
                             names=series_names,
                             plotstyles=styles.SERIES_ALT,
                             plotparams='bg')

        for metric in metrics:
            # bars = [grouped[metric].min(), grouped[metric].max()]

            series = agg2series(grouped[metric].mean(),
                                names=series_names,
                                #errs=dict(e_abs=bars),
                                #plotparams='fg-e')
                                plotparams='fg')

            ax = plot.variants(series,
                               xgrid=grids.x.budget,
                               ygrid=grids.y.get(metric))
            save('scheduler', exp_id, '{}-7hybrid-b{:g}'.format(metric, budget))

            ax1, ax2 = plot.variants_dual(series, series2,
                                          xgrid=grids.x.num_apps,
                                          ygrid=grids.y.get(metric),
                                          ygrid2=grids.y.fps)

            plt.tight_layout()

            save('scheduler', exp_id, '{}-7hybrid-dual-b{:g}'.format(metric, budget))


def metric_7hybrid_by_budget(metrics=['f1']):
    exp_id = "050318"
    series_names = ["mainstream", "maxsharing", "nosharing"]

    df = _get_data(exp_id, series_names)

    for num_apps in set(df['num_apps'].values):
        df_view = df[df['num_apps'] == num_apps]
        grouped = df_view.groupby(['sharing', 'budget'])

        series2 = agg2series(grouped['fps'].mean(),
                             names=series_names,
                             plotstyles=styles.SERIES_ALT,
                             plotparams='bg')

        for metric in metrics:
            series = agg2series(grouped[metric].mean(),
                                names=series_names,
                                plotparams='fg')

            ax = plot.variants(series,
                               xgrid=grids.x.budget,
                               ygrid=grids.y.get(metric))
            save('scheduler', exp_id, '{}-7hybrid-n{:g}'.format(metric, num_apps))

            ax1, ax2 = plot.variants_dual(series, series2,
                                          xgrid=grids.x.budget,
                                          ygrid=grids.y.get(metric),
                                          ygrid2=grids.y.fps)
            legends.dual_fps(ax1, ax2, left=metric.capitalize(), loc='upper left')

            save('scheduler', exp_id, '{}-7hybrid-dual-n{:g}'.format(metric, num_apps))


def f1_7hybrid_annotated():
    budget = 150
    exp_id = "050318"
    series_names = ["mainstream", "maxsharing", "nosharing"]

    df = _get_data(exp_id, series_names)

    df_view = df[df['budget'] == budget]
    grouped = df_view.groupby(['sharing', 'num_apps'])

    series_fps = agg2series(grouped['fps'].mean(), names=series_names)
    series_acc = agg2series(1. - grouped['rel_acc'].mean(), names=series_names)

    series = agg2series(grouped['f1'].mean(),
                        names=series_names,
                        plotparams='fg')

    ax = plot.variants(series,
                       xgrid=grids.x.num_apps,
                       ygrid=grids.y.f1,
                       legend=legends.above_fig)

    annotations = [
        [Annotation(pt=1, xy=(10, 30), name='a', arrow_kwargs=dict(shrinkA=3), va='center'),
         Annotation(pt=10, xy=(-50, 18), name='b', arrow_kwargs=dict(shrinkA=5), ha='center')],
        [Annotation(pt=1, xy=(15, 25), name='c', va='center'),
         Annotation(pt=10, xy=(-55, -20), name='d', ha='center', va='top')],
        [Annotation(pt=1, xy=(25, -16), name='e', va='center'),
         Annotation(pt=10, xy=(-45, 30), name='f', arrow_kwargs=dict(shrinkA=5), ha='center')],
    ]

    add_annotations(annotations,
                    series,
                    fmt_str="({name}) Frame Rel Acc: {acc:.2g}, FPS: {fps:.2g}",
                    extra={'fps': series_fps, 'acc': series_acc},
                    ax=ax)
    save('scheduler', exp_id, '{}-7hybrid-annotated-b{:g}'.format("f1", 150), bbox_inches="tight")


def main():
    # f1_7hybrid_annotated()
    # metric_7hybrid(metrics=['f1', 'recall', 'precision'])
    metric_7hybrid_by_budget(metrics=['f1', 'recall', 'precision'])


if __name__ == '__main__':
    main()
