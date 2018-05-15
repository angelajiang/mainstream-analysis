# Usage: python -m scripts.scheduler.7hybrid
import dataloaders
import plot
from plotutils import ex, comb, agg2series
from plotutils import legends
from plotutils import styles
from plotutils import grids
from utils import save


def metric_7hybrid(metrics=['f1']):
    exp_id = "050318"
    series_names = ["mainstream", "maxsharing", "nosharing"]

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
                   each=lambda s: s.to_map(),
                   constant={'scheduler': 'greedy', 'sharing': series_name})
    df = comb(rows)

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
            bars = [grouped[metric].min(), grouped[metric].max()]

            series = agg2series(grouped[metric].mean(),
                                names=series_names,
                                errs=dict(e_abs=bars),
                                plotparams='fg-e')

            ax1, ax2 = plot.variants_dual(series, series2,
                                          xgrid=grids.x.num_apps,
                                          y1grid=grids.y.get(metric),
                                          y2grid=grids.y.fps)
            legends.dual_fps(ax1, ax2, left=metric.capitalize())
            save('scheduler', exp_id, '{}-7hybrid-dual-b{:g}'.format(metric, budget))


def main():
    metric_7hybrid(metrics=['f1', 'recall', 'precision'])


if __name__ == '__main__':
    main()
