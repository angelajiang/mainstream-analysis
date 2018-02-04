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
root_dir = "output/streamer/scheduler/atc"
metric = "f1"
comb_files_loc = root_dir + "/{metric}/{metric}-combinations-*-mainstream-simulator".format(metric=metric)
comb_file_name = collect_comb_csvs(comb_files_loc)
ms0 = comb_file_name
ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-mainstream-simulator"
max1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-maxsharing"
min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-nosharing"
f1 ="f1-4hybrid"
t1 = ""
ms_files = [ms0, ms1]
max_files = [max1]
min_files = [min1]
f_files = [f1]
titles = [t1]
hybrid4_annotations = [1, 6, 1, 5, 3, 6]
plot_dir = "plots/scheduler/atc/maximize-f1"
plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, annotations = hybrid4_annotations)
plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)


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


