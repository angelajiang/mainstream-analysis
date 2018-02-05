#!/bin/bash

PLOT_DIR=../mainstream-paper/atc2018/figures/plots

# Fig 5: Effect of sample-rate on recall
# python scripts/goodness/false_neg_by_stride.py
cp plots/frame-rate/frame-rate-afn-dependences-with-correlation.pdf $PLOT_DIR

# Fig 10: deploy-time-series
# python scripts/deploy/visualize.py
cp plots/deploy/deploy-time-series.pdf $PLOT_DIR
