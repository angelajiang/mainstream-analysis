import matplotlib.pyplot as plt

# TODO: default_kwargs
default_kwargs = dict()


def dual_fps(ax1, ax2, left='??', right='FPS'):
    leg = ax1.legend(loc=4, bbox_to_anchor=[.84, .1], fontsize=13, borderpad=None)
    leg2 = ax2.legend(loc=4, bbox_to_anchor=[.99, .1], fontsize=13, borderpad=None)
    for txt in leg.get_texts():
        txt.set_text(txt.get_text() + ' ' + left)
    for txt in leg2.get_texts():
        txt.set_text(right)
    leg.get_frame().set_facecolor('white')
    leg.get_frame().set_linewidth(0.)
    leg2.get_frame().set_facecolor('white')
    leg2.get_frame().set_linewidth(0.)


above_fig_kwargs = dict(bbox_to_anchor=(0.5, 1.2),
                        frameon=False,
                        fontsize=12, ncol=3, loc='upper center')


def above_fig(ax):
    ax.legend(**above_fig_kwargs)


def ncol(ax=None, ncol=2, fontsize=10, loc='lower center', **kwargs):
    if ax is None:
        ax = plt.gca()
    kwargs['ncol'] = ncol
    kwargs['fontsize'] = fontsize
    kwargs['loc'] = loc
    ax.legend(**kwargs)
