#!/bin/bash

PLOT_DIR=../../mainstream-paper/atc2018-camera/figures/plots

# Fig 4a task-throughput
cp plots/sharing/task_throughput.pdf $PLOT_DIR/
# Fig 4b Per-frame accuracy vs. (potential) sharing
cp plots/sharing/7hybrid-multi-network-accuracy.pdf $PLOT_DIR/7hybrid/accuracy

# Fig 5: Effect of sample-rate on recall
cp plots/correlations/recall-samplerate-train.pdf $PLOT_DIR/frame-rate-afn-dependences-with-correlation.pdf

# Fig 6: F1 for no of concurrent apps
cp plots/scheduler/050318/f1-7hybrid-annotated-b150.pdf $PLOT_DIR/7hybrid/sweep

# Fig 7: dual
cp plots/scheduler/050318/f1-7hybrid-dual-b300.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/recall-7hybrid-dual-b300.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/precision-7hybrid-dual-b300.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/f1-7hybrid-dual-b150.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/recall-7hybrid-dual-b150.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/precision-7hybrid-dual-b150.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/f1-7hybrid-b150.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/recall-7hybrid-b150.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/050318/precision-7hybrid-b150.pdf $PLOT_DIR/7hybrid/sweep
cp plots/scheduler/legend.pdf $PLOT_DIR

# New Fig 8
cp plots/scheduler/050318/f1-7hybrid-dual-n3.pdf $PLOT_DIR/7hybrid/budget

# # Fig 8: corr
# cp plots/scheduler/050318-corr/f1-7hybrid-corr_dep-dual-b300.pdf $PLOT_DIR/7hybrid/correlation
# cp plots/scheduler/050318-corr/f1-7hybrid-corr_emp-dual-b300.pdf $PLOT_DIR/7hybrid/correlation
# cp plots/scheduler/050318-corr/f1-7hybrid-corr_ind-dual-b300.pdf $PLOT_DIR/7hybrid/correlation
# cp plots/scheduler/050318-corr/f1-7hybrid-corr_dep-b150.pdf $PLOT_DIR/7hybrid/correlation
# cp plots/scheduler/050318-corr/f1-7hybrid-corr_emp-b150.pdf $PLOT_DIR/7hybrid/correlation
# cp plots/scheduler/050318-corr/f1-7hybrid-corr_ind-b150.pdf $PLOT_DIR/7hybrid/correlation
# cp plots/scheduler/legend_f1.pdf $PLOT_DIR

# Fig 9: x-voting
cp plots/scheduler/x_voting/train-f1-f1-1357-frontier.pdf $PLOT_DIR/scheduler/voting-train-500-f1-f1-frontier.pdf

# Fig 10: deploy-time-series
cp ../pre-2018-Spring/plots/deploy/deploy-time-series.pdf $PLOT_DIR
