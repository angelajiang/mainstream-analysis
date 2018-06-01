#!/bin/bash

PLOT_DIR=../mainstream-paper/atc2018/figures/plots

# Fig 5: Effect of sample-rate on recall
# python scripts/goodness/false_neg_by_stride.py
cp plots/frame-rate/frame-rate-afn-dependences-with-correlation.pdf $PLOT_DIR

# Fig 6: F1 for no of concurrent apps
# python scripts/generate_atc_graphs.py
cp plots/scheduler/atc/maximize-f1/f1-4hybrid-f1-annotated.pdf $PLOT_DIR/scheduler

# Fig 7: dual
# python scripts/generate_atc_graphs.py
cp plots/scheduler/atc/maximize-f1/f1-4hybrid-f1-dual.pdf $PLOT_DIR/scheduler
cp plots/scheduler/atc/maximize-f1/f1-4hybrid-recall-dual.pdf $PLOT_DIR/scheduler
cp plots/scheduler/atc/maximize-f1/f1-4hybrid-precision-dual.pdf $PLOT_DIR/scheduler

# Fig 8: corr
# python scripts/generate_atc_graphs.py
cp plots/scheduler/atc/maximize-f1/f1-4hybrid-corr0-f1.pdf $PLOT_DIR/scheduler/0-correlation.pdf
cp plots/scheduler/atc/maximize-f1/f1-4hybrid-corr-emph-f1.pdf $PLOT_DIR/scheduler/empirical-correlation.pdf
cp plots/scheduler/atc/maximize-f1/f1-4hybrid-corr1-f1.pdf $PLOT_DIR/scheduler/1-correlation.pdf

# Fig 10: deploy-time-series
# python scripts/deploy/visualize.py
cp plots/deploy/deploy-time-series.pdf $PLOT_DIR
