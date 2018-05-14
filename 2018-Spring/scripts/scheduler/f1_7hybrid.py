# Each function does one plot
# Also an example of a script that would appear in a python notebook
import dataloaders
import plot
from plotutils import ex, comb, agg2series, get_errors
from plotutils import legends
from plotutils import grids
from plotutils import styles
from utils import save
from utils import mean


def f1_7hybrid():
    exp_id = "050318"
    series_names = ["mainstream", "maxsharing", "nosharing"]

    setups = dataloaders.load_setups(exp_id, setup_file_str="/setups.{exp_id}-*{version}.pickle")

    rows = []
    for series_name in series_names:
        schedules = dataloaders.load_schedules("050318", "greedy." + series_name + ".sim.*.v1", setups=setups)
        # Extract some attributes from the schedules.
        # Add on some based on the file name.
        rows += ex(schedules,
                   each=lambda s: {'f1': mean(s.f1s), 'fps': mean(s.fpses), 'num_apps': s.num_apps, 'budget': s.budget},
                   constant={'scheduler': 'greedy', 'sharing': series_name})
    df = comb(rows)

    # See Pandas: Group By: split-apply-combine
    # https://pandas.pydata.org/pandas-docs/stable/groupby.html
    for budget in set(df['budget'].values):
        df_view = df[df['budget'] == budget]
        # Group <setups> by number of apps, aggregate by mean.
        grouped = df_view.groupby(['sharing', 'num_apps'])

        bars = [grouped['f1'].min(), grouped['f1'].max()]

        series = agg2series(grouped['f1'].mean(),
                            names=series_names,
                            yerrs=get_errors(e_abs=bars),
                            plotparams=dict(lw=4, markersize=8))

        series2 = agg2series(grouped['fps'].mean(),
                             names=series_names,
                             plotstyles=styles.SERIES_ALT,
                             plotparams=dict(lw=3, markersize=8, alpha=0.7, linestyle='--'))

        ax1, ax2 = plot.variants_dual(series, series2,
                                      xgrid=grids.x.num_apps,
                                      y1grid=grids.y.f1,
                                      y2grid=grids.y.fps)
        legends.dual_fps(ax1, ax2, left='F1')
        save('scheduler', exp_id, 'f1-7hybrid-dual-b{}'.format(budget))


if __name__ == '__main__':
    f1_7hybrid()
