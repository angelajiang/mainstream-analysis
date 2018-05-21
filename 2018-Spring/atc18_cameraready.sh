#!/bin/bash

PLOT_DIR=../../mainstream-paper/atc2018-camera/figures/plots

# Fig 4a task-throughput
cp plots/sharing/task_throughput.pdf $PLOT_DIR/
# Fig 4b Per-frame accuracy vs. (potential) sharing
cp plots/sharing/7hybrid-mobilenets-accuracy.pdf $PLOT_DIR/

# Fig 5: Effect of sample-rate on recall
# python scripts/goodness/false_neg_by_stride.py
# cp plots/frame-rate/frame-rate-afn-dependences-with-correlation.pdf $PLOT_DIR

# Fig 6: F1 for no of concurrent apps
cp plots/scheduler/050318/f1-7hybrid-annotated-b150.pdf $PLOT_DIR/7hybrid/sweep

# Fig 7: dual
cp plots/scheduler/050318/f1-7hybrid-dual-b300.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/recall-7hybrid-dual-b300.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/precision-7hybrid-dual-b300.pdf $PLOT_DIR/7hybrid/sweep

# Fig 8: corr
cp plots/scheduler/050318-corr/f1-7hybrid-corr_dep-dual-b300.pdf $PLOT_DIR/7hybrid/correlation
cp plots/scheduler/050318-corr/f1-7hybrid-corr_emp-dual-b300.pdf $PLOT_DIR/7hybrid/correlation
cp plots/scheduler/050318-corr/f1-7hybrid-corr_ind-dual-b300.pdf $PLOT_DIR/7hybrid/correlation

# Fig 10: deploy-time-series
# python scripts/deploy/visualize.py
# cp plots/deploy/deploy-time-series.pdf $PLOT_DIR
