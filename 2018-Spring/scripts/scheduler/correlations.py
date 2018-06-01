import matplotlib.pyplot as plt
import dataloaders
import plot
from plotutils import ex, comb, agg2series
from plotutils import legends
from plotutils import styles
from plotutils import grids
from utils import save, memoize


@memoize()
def _get_data(exp_id, series_names, corr_types):
    # Overriding setup_file_str because dir was renamed to have -corr
    setups = dataloaders.load_setups(exp_id,
                                     setup_file_str="/setups.*{version}.pickle")
    rows = []
    for series_name in series_names:
        for corr in corr_types:
            schedules = dataloaders.load_schedules(exp_id,
                                                   "greedy." + series_name + ".sim.*-" + corr + ".v1",
                                                   setups=setups)
            rows += ex(schedules,
                       constant={'scheduler': 'greedy', 'sharing': series_name, 'correlation': corr})
    df = comb(rows)
    return df


def correlations_7hybrid():
    exp_id = "050318-corr"
    series_names = ["mainstream", "maxsharing", "nosharing"]
    corr_types = ["ind", "emp", "dep"]
    metrics = ["f1"]

    df = _get_data(exp_id, series_names, corr_types)

    for corr in corr_types:
        for budget in set(df['budget'].values):
            df_view = df[(df['budget'] == budget) & (df['correlation'] == corr)]

            grouped = df_view.groupby(['sharing', 'num_apps'])

            series2 = agg2series(grouped['fps'].mean(),
                                 names=series_names,
                                 plotstyles=styles.SERIES_ALT,
                                 plotparams='bg')

            for metric in metrics:
                series = agg2series(grouped[metric].mean(),
                                    names=series_names,
                                    plotparams='fg')

                ax = plot.variants(series,
                                   xgrid=grids.x.num_apps,
                                   ygrid=grids.y.get(metric))

                save('scheduler', exp_id, '{}-7hybrid-corr_{}-b{:g}'.format(metric, corr, budget))
                plt.close()

                ax1, ax2 = plot.variants_dual(series, series2,
                                              xgrid=grids.x.num_apps,
                                              ygrid=grids.y.get(metric),
                                              ygrid2=grids.y.fps)
                # legends.dual_fps(ax1, ax2, left=metric.capitalize())
                legends.hide(ax1, ax2)

                save('scheduler', exp_id, '{}-7hybrid-corr_{}-dual-b{:g}'.format(metric, corr, budget))
                plt.close()


def main():
    correlations_7hybrid()


if __name__ == '__main__':
    main()
