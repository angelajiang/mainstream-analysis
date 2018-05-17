import os
import matplotlib.pyplot as plt
from constants import PLOT_DIR


def save(group='', exp_id='', plot_id='', plot_dir=PLOT_DIR, **kwargs):
    if not os.path.exists(os.path.join(plot_dir, group, exp_id)):
        os.makedirs(os.path.join(plot_dir, group, exp_id))
    save_exact(os.path.join(plot_dir, group, exp_id, plot_id), **kwargs)


def save_exact(filename, pdf=True, png=False, **kwargs):
    if pdf:
        plt.savefig(filename + ".pdf", **kwargs)
    if png:
        plt.savefig(filename + ".png", dpi=72, **kwargs)
