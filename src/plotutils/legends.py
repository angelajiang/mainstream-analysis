import matplotlib as mpl
import matplotlib.pyplot as plt


def legendsize(scale=1.):
    return mpl.rcParams['legend.fontsize'] * scale


def dual_fps_old(ax1, ax2, left='??', right='FPS'):
    common_params = dict(loc=4, fontsize=legendsize(.7), borderpad=None)
    leg = ax1.legend(bbox_to_anchor=[.84, .1], **common_params)
    leg2 = ax2.legend(bbox_to_anchor=[.99, .1], **common_params)
    for txt in leg.get_texts():
        txt.set_text(txt.get_text() + ' ' + left)
    for txt in leg2.get_texts():
        txt.set_text(right)
    leg.get_frame().set_facecolor('white')
    leg.get_frame().set_linewidth(0.)
    leg2.get_frame().set_facecolor('white')
    leg2.get_frame().set_linewidth(0.)


def dual_fps(ax1, ax2, left='??', right='FPS', **kwargs):
    lines = ax1.lines + ax2.lines
    labels = [(l.get_label() + ' ' + left if i < len(ax1.lines) else right) for i, l in enumerate(lines)]

    ax1.legend(lines, labels, ncol=2, fontsize=legendsize(.7), **kwargs)
    ax2.legend().set_visible(False)


def separate_dual(ax1, ax2, left='???', right='FPS'):
    reorder = [0, 3, 1, 4, 2, 5]
    lines = ax1.lines + ax2.lines
    assert len(lines) == 6, lines
    labels = [l.get_label() + (' ' + left if i < len(ax1.lines) else ' ' + right) for i, l in enumerate(lines)]
    lines = [lines[i] for i in reorder]
    labels = [labels[i] for i in reorder]
    fig = plt.figure(figsize=(3, 2))
    legend = plt.legend(lines, labels, ncol=3, loc='center')
    plt.axis('off')
    fig.canvas.draw()
    return dict(bbox_inches=legend.get_window_extent().transformed(fig.dpi_scale_trans.inverted()), pad_inches=0)


def above_fig(ax):
    above_fig_kwargs = dict(bbox_to_anchor=(0.5, 1.2),
                            frameon=False,
                            fontsize=legendsize(), ncol=3, loc='upper center')
    ax.legend(**above_fig_kwargs)


def reversed(ax):
    handles, labels = ax.get_legend_handles_labels()
    ax.legend(handles[::-1], labels[::-1])


def ncol(ax=None, ncol=2, fontsize=.7, loc='lower center', **kwargs):
    if ax is None:
        ax = plt.gca()
    kwargs['ncol'] = ncol
    kwargs['fontsize'] = legendsize(fontsize)
    kwargs['loc'] = loc
    ax.legend(**kwargs)


def hide(*axes):
    for ax in axes:
        ax.legend().set_visible(False)
