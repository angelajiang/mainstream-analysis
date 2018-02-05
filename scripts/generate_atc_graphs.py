import sys
sys.path.append("scripts/scheduler")
import scheduler
import scheduler_dual
from data_util import collect_comb_csvs



################## Maximize F1 Score ##################
plot_dir = "plots/scheduler/atc/maximize-f1"
t1 = ""

def f1_pedestrian():
    ms1 =  "output/streamer/scheduler/atc/f1/f1-pedestrian-500-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-pedestrian-500-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-pedestrian-500-nosharing"
    f1 ="f1-pedestrian-500"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]
    pedestrian_annotations = [5, 28, 2, 15, 1, 20]

    # scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, annotations = pedestrian_annotations)
    scheduler_dual.plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_recall_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_precision_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)


def f1_train_500():
    ms1 =  "output/streamer/scheduler/atc/f1/f1-train-500-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-train-500-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-train-500-nosharing"
    f1 ="f1-train-500"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    f_files_annotated = [f + "-annotated" for f in f_files]
    titles = [t1]

    scheduler_dual.plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_recall_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_precision_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)


def f1_4hybrid():
    ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-nosharing"
    f1 ="f1-4hybrid"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    titles = [t1]
    hybrid4_annotations = [2, 6, 1, 5, 0, 6]
    hybrid4_annotations = [i+2 for i in hybrid4_annotations]

    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, annotations = hybrid4_annotations, errbars=False)
    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, errbars=False)
    scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_recall_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler_dual.plot_precision_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)

f1_pedestrian()
f1_train_500()
f1_4hybrid()

############## COMBINATIONS ############
# scheduler.run_combinations()

############## X-voting ############
scheduler.run_x_voting()

############## Fairness ############
# scheduler.run_fairness()

############## CONDITIONAL PROBABILITY ############

def f1_4hybrid_corr0():
    ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-corr0-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr0-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr0-nosharing"
    f1 ="f1-4hybrid-corr0"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    titles = [t1]

    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)


def f1_4hybrid_corr_emph():
    ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-nosharing"
    f1 ="f1-4hybrid-corr-emph"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    titles = [t1]

    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, errbars=False)
    scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir, errbars=False)


def f1_4hybrid_corr1():
    ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-corr1-mainstream-simulator"
    max1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr1-maxsharing"
    min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr1-nosharing"
    f1 ="f1-4hybrid-corr1"

    ms_files = [ms1]
    max_files = [max1]
    min_files = [min1]
    f_files = [f1]
    titles = [t1]

    scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
    scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)

f1_4hybrid_corr0()
f1_4hybrid_corr_emph()
f1_4hybrid_corr1()