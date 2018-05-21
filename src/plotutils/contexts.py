# Similar to seaborn contexts (https://seaborn.pydata.org/tutorial/aesthetics.html)
# See https://github.com/mwaskom/seaborn/blob/master/seaborn/rcmod.py
import matplotlib as mpl


def single():
    """Default: for 1:1 meetings, presenting just one graph"""
    return {
        'axes.titlesize': 24,
        'axes.labelsize': 20,
        'lines.linewidth': 3,
        'lines.markersize': 10,
        'xtick.labelsize': 15,
        'ytick.labelsize': 15,
        'legend.fontsize': 13,

        'mathtext.fontset': 'custom',
        'mathtext.rm': 'Bitstream Vera Sans',
        'mathtext.it': 'Bitstream Vera Sans:italic',
        'mathtext.bf': 'Bitstream Vera Sans:bold',
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
    return rescale(single(), factor=1.1)


def paper():
    return rescale(single(), factor=.9)


def rescale(params, factor=1.):
    return {k: v * factor if k.endswith('size') else v
            for k, v in params.items()}


def use(name):
    if isinstance(name, str):
        name = globals()[name]
    mpl.rcParams.update(name())


use('single')
