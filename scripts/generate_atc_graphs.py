import sys
sys.path.append("scripts/scheduler")
import scheduler


plot_dir = "plots/scheduler/atc/correlation"
f1 ="recall-maxsharing"

max1 = "output/streamer/scheduler/atc/recall/recall-pedestrian-corr0.3-maxsharing" 
max2 = "output/streamer/scheduler/atc/recall/recall-pedestrian-corr0-maxsharing" 
max3 = "output/streamer/scheduler/atc/recall/recall-pedestrian-corr1-maxsharing" 
l1 = "Empirical"
l2 = "Fully uncorrelated"
l3 = "Fully correlated"

scheduler.plot_correlation([max1, max2, max3], [l1, l2, l3], f1, plot_dir)

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

scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, annotated=True)
scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir, version=1)
scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)

plot_dir = "plots/scheduler/atc/maximize-f1"
t1 = ""

ms1 =  "output/streamer/scheduler/atc/f1/f1-cars-500-mainstream-simulator"
max1 = "output/streamer/scheduler/atc/f1/f1-cars-500-maxsharing"
min1 = "output/streamer/scheduler/atc/f1/f1-cars-500-nosharing"
f1 ="f1-cars-500"

ms_files = [ms1]
max_files = [max1]
min_files = [min1]
f_files = [f1]
f_files_annotated = [f + "-annotated" for f in f_files]
titles = [t1]

scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir, version=1)
scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)

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

scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir, annotated=True)
scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir, version=1)
scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)

ms1 =  "output/streamer/scheduler/atc/f1/f1-cats-2000-mainstream-simulator"
max1 = "output/streamer/scheduler/atc/f1/f1-cats-2000-maxsharing"
min1 = "output/streamer/scheduler/atc/f1/f1-cats-2000-nosharing"
f1 ="f1-cats-2000"

ms_files = [ms1]
max_files = [max1]
min_files = [min1]
f_files = [f1]
f_files_annotated = [f + "-annotated" for f in f_files]
titles = [t1]

scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir, version=1)
scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)

ms1 =  "output/streamer/scheduler/atc/f1/f1-3hybrid-mainstream-simulator"
max1 = "output/streamer/scheduler/atc/f1/f1-3hybrid-maxsharing"
min1 = "output/streamer/scheduler/atc/f1/f1-3hybrid-nosharing"
f1 ="f1-3hybrid"

ms_files = [ms1]
max_files = [max1]
min_files = [min1]
f_files = [f1]
f_files_annotated = [f + "-annotated" for f in f_files]
titles = [t1]

scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir, version=1)
scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)

ms1 =  "output/streamer/scheduler/atc/f1/f1-4hybrid-mainstream-simulator"
max1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-maxsharing"
min1 = "output/streamer/scheduler/atc/f1/f1-4hybrid-nosharing"
f1 ="f1-4hybrid"

ms_files = [ms1]
max_files = [max1]
min_files = [min1]
f_files = [f1]
f_files_annotated = [f + "-annotated" for f in f_files]
titles = [t1]

scheduler.plot_f1(ms_files, max_files, min_files, f_files, titles, plot_dir)
scheduler.plot_recall(ms_files, max_files, min_files, f_files, titles, plot_dir, version=1)
scheduler.plot_precision(ms_files, max_files, min_files, f_files, titles, plot_dir)
