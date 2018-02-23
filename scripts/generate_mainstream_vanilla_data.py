import sys
sys.path.append("scripts/scheduler")
import scheduler
import scheduler_dual
from data_util import collect_comb_csvs



################## Maximize F1 Score ##################
plot_dir = "plots/scheduler/atc/maximize-f1"
t1 = ""

def f1_4hybrid():
    ms1 =  "output/streamer/scheduler/atc/f1/combos/f1-4hybrid-combo-all-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/combos/f1-4hybrid-combo-all-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/combos/f1-4hybrid-combo-all-nosharing"
    f1 ="f1-4hybrid"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    titles = [t1]
    hybrid4_annotations = []
#    hybrid4_annotations = [2, 6, 1, 5, 0, 6]
#    hybrid4_annotations = [i+2 for i in hybrid4_annotations]  # Because of left 2 points added.

    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir,
                      annotations = hybrid4_annotations, errbars=False, legend_xargs=dict(loc=3))
    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, errbars=False)
    scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_recall_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_precision_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)

f1_4hybrid()

