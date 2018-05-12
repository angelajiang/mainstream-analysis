# Each function does one plot
# Also an example of a script that would appear in a python notebook
import dataloaders
import plot
from plotutils import Series
from plotutils import ex, comb
from plotutils import colors
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
    df_view = df[df['budget'] == 100]
    # Group <setups> by number of apps, aggregate by mean.
    grouped = df_view.groupby(['sharing', 'num_apps'])

    aggregated = grouped['f1'].mean()
    unstacked = aggregated.unstack(0)
    xss, yss = zip(*[(unstacked[k].index, unstacked[k].values) for k in series_names])
    series = [Series(x=xs, y=ys, name=sn, plotstyle=sn) for xs, ys, sn in zip(xss, yss, series_names)]

    plotparams = dict(lw=4, markersize=8)
    plot.variants(series, plot_kwargs=plotparams)
    plot.save('scheduler', exp_id, 'f1')


if __name__ == '__main__':
    f1_7hybrid()
