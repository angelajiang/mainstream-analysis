# Similar to seaborn contexts (https://seaborn.pydata.org/tutorial/aesthetics.html)
# See https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py
import matplotlib as mpl


def single():
    """Default: for 1:1 meetings, presenting just one graph"""
    return {
        'font.size': 14,
        'axes.titlesize': 22,
        'axes.labelsize': 23,
        'lines.linewidth': 3,
        'lines.markersize': 8,
        'xtick.labelsize': 20,
        'ytick.labelsize': 20,
        'legend.fontsize': 16,

        'mathtext.fontset': 'custom',
        'mathtext.rm': 'Bitstream Vera Sans',
        'mathtext.it': 'Bitstream Vera Sans:italic',
        'mathtext.bf': 'Bitstream Vera Sans:bold',

        'legend.columnspacing': .8,
        'legend.frameon': False,
    }


def double():
    """When you have to squeeze in 2 graphs into one slide"""
    return rescale(single(), factor=1.8)


def triple():
    """When you have to squeeze in 3 graphs into one slide"""
    return rescale(single(), factor=1.9)


def poster():
    raise NotImplementedError
    return rescale(single(), factor=2.)


def notebook():
    return rescale(single(), factor=1.)


def paper():
    return rescale(single(), factor=1.)


def rescale(params, factor=1.):
    return {k: v * factor if k.endswith('size') else v
            for k, v in params.items()}


def get(prop):
    return mpl.rcParams[prop]


def use(name):
    if isinstance(name, str):
        name = globals()[name]
    mpl.rcParams.update(name())


use('single')
