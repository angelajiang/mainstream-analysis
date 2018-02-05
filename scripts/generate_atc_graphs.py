import sys
sys.path.append("scripts/scheduler")
import scheduler
import scheduler_dual


################## Maximize F1 Score ##################

plot_dir = "plots/scheduler/atc/maximize-f1"
t1 = ""

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

#scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, annotations = pedestrian_annotations)
scheduler_dual.plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler_dual.plot_recall_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler_dual.plot_precision_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)

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

scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, annotations = hybrid4_annotations)
scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler_dual.plot_f1_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler_dual.plot_recall_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler_dual.plot_precision_dual(ms_files, max_files, min_files, f_files, titles, plot_dir)


############## COMBINATIONS ############
scheduler.run_combinations()

############## COMBINATIONS ############
scheduler.run_combinations_left4pts()

############## Fairness ############
scheduler.run_fairness()

############## CONDITIONAL PROBABILITY ############

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

ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-mainstream-simulator"
max1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-maxsharing"
min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-corr-emph-nosharing"
f1 ="f1-4hybrid-corr-emph"

ms_files = [ms1]
max_files = [max1]
min_files = [min1]
f_files = [f1]
titles = [t1]

scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)

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


