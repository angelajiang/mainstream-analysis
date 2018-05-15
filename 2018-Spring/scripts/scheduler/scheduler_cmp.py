# Usage: python -m scripts.scheduler.scheduler_cmp
import dataloaders
import plot
from plotutils import ex, comb, agg2series
from plotutils import legends
from plotutils import grids
from plotutils import styles
from utils import save


def scheduler_cmp():
    exp_id = "050318"
    series_names = ["greedy", "stems_cpp", "exhaustive"]

    setups = dataloaders.load_setups(exp_id,
                                     setup_file_str="/setups.{exp_id}-*{version}.pickle",
                                     legacy='InconsistentIds')

    variants = {
        'greedy': 'v1+metrics',
        'exhaustive': 'v1+cost',
        'stems_cpp': None,
    }
    rows = []
    for series_name in series_names:
        if series_name == 'exhaustive':
            scheduleloader_kwargs = dict(apps_order='configurations')
        else:
            scheduleloader_kwargs = {}

        schedules = dataloaders.load_schedules("050318",
                                               series_name + ".mainstream.sim.*.v1",
                                               variant=variants[series_name],
                                               setups=setups,
                                               **scheduleloader_kwargs)

        rows += ex(schedules, constant={'scheduler': series_name, 'sharing': 'mainstream'})
    df = comb(rows)

    metric = 'f1'
    for budget in set(df['budget'].values):
        df_view = df[df['budget'] == budget]
        grouped = df_view.groupby(['scheduler', 'num_apps'])

        bars = [grouped[metric].min(), grouped[metric].max()]

        series = agg2series(grouped[metric].mean(),
                            names=series_names,
                            errs=dict(e_abs=bars),
                            plotparams='fg-e')

        ax = plot.variants(series,
                           xgrid=grids.x.num_apps,
                           ygrid=grids.y.get(metric))
        save('scheduler', exp_id, 'schedulers_cmp-7hybrid-b{:g}'.format(budget))


if __name__ == '__main__':
    scheduler_cmp()
