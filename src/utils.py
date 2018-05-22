from __future__ import print_function
import sys
import os
import matplotlib.pyplot as plt
from constants import PLOT_DIR


def save(group='', exp_id='', plot_id='', plot_dir=PLOT_DIR, **kwargs):
    if not os.path.exists(os.path.join(plot_dir, group, exp_id)):
        os.makedirs(os.path.join(plot_dir, group, exp_id))
    save_exact(os.path.join(plot_dir, group, exp_id, plot_id), **kwargs)


def save_exact(filename, pdf=True, png=False, **kwargs):
    rel_filename = filename.replace(os.getcwd() + "/", "")
    # set CreationDate to allow for deterministic PDFs to aid inclusion in git
    if pdf:
        plt.savefig(filename + ".pdf", metadata={'creationDate': None}, **kwargs)
        print(rel_filename + ".pdf saved", file=sys.stderr)
    if png:
        plt.savefig(filename + ".png", metadata={'creationDate': None}, dpi=72, **kwargs)
        print(rel_filename + ".png saved", file=sys.stderr)
