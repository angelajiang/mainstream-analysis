import sys
sys.path.append("scripts/scheduler")
import scheduler
import scheduler_dual
from data_util import collect_comb_csvs
from itertools import combinations


################## Maximize F1 Score ##################
plot_dir = "plots/scheduler/distributed/f1/"
t1 = ""

def f1_combos(k):
    apps = ['cars', 'cats', 'pedestrian', 'train', 'flowers']

    combos = combinations(apps, k)
    filename_format = 'output/streamer/scheduler/distributed/f1/mobilenets/f1-{}-500-mainstream-simulator'

    files = []
    labels = []
    for combo in combos:
        complement = [x for x in apps if x not in combo]

        filename = filename_format.format('-'.join(combo))
        comp_filename = filename_format.format('-'.join(complement))
        label = '{' + '-'.join(combo) + ',' + '-'.join(complement) + '}'
        files.append([filename,comp_filename])
        labels.append(label)
    scheduler.plot_distributed(files, labels, str(k) + '-combos-4hybrid', plot_dir, average_weights=[k, len(apps) - k])

f1_combos(2)
f1_combos(3)
f1_combos(4)
f1_combos(1)
