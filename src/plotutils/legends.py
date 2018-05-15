
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
