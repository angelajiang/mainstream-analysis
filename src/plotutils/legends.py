
def dual_fps(ax1, ax2, left='??', right='FPS'):
    labels = [l.get_label() + ' {}'.format(left) for l in ax1.lines]
    leg = ax1.legend(ax1.lines, labels, loc=4, bbox_to_anchor=[.84, .1], fontsize=13, borderpad=None)
    leg2 = ax2.legend(ax2.lines, [right] * len(ax1.lines), loc=4, bbox_to_anchor=[.99, .1], fontsize=13, borderpad=None)
    leg.get_frame().set_facecolor('white')
    leg.get_frame().set_linewidth(0.0)
    leg2.get_frame().set_facecolor('white')
    leg2.get_frame().set_linewidth(0.0)
