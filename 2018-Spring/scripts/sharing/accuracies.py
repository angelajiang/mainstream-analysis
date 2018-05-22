import dataloaders
import plot
import plotutils
from plotutils import grids
from plotutils import legends
from plotutils import styles
from utils import save


def plotstyle(label, **kwargs):
    kwargs['label'] = label
    colourmatch = {
        'Red': '#FE1310',
        'Schoolbus': '#FFB019',
        'Flowers': '#ED2363',
        'Scramble': '#808080',
        'Bus': '#2881B9',
        'Pedestrian': '#8EF9FF',
        'Cats': '#BF8D4A',
        'Cars': '#D5E625',
    }
    for k, v in colourmatch.items():
        if label.startswith(k):
            kwargs['color'] = v
    return kwargs


def mpackages2series(mpackages):
    pp = dict(styles.LINEGROUPS['fg'])
    pp['alpha'] = .8
    return [plotutils.Series(y=p_.accuracies.acc,
                             x=p_.accuracies.num_frozen_percent,
                             name=p_.label,
                             plotstyle=plotstyle(p_.label, marker=marker, ms=ms),
                             plotparams=pp)
            for p_, marker, ms in zip(mpackages, styles.MARKERS, styles.MARKERSIZES)]


def _plot(packages):
    return plot.variants(mpackages2series(packages),
                         order='y',
                         xgrid=grids.x.frozen,
                         ygrid=grids.y.accuracy)


def mobilenets_8hybrid():
    packages = dataloaders.MPackage.filter(architecture='mobilenets')
    assert len(packages) == 8, len(packages)
    ax = _plot(packages)
    legends.ncol(ax)
    save(group='sharing', plot_id='{}-{}-accuracy'.format("7hybrid", "mobilenets"))


def inception():
    packages = dataloaders.MPackage.filter(architecture='inception',
                                           dataset=['bus', 'cars'])
    assert len(packages) == 2
    _plot(packages)
    save(group='sharing', plot_id='{}-{}-accuracy'.format("2hybrid", "inception"))


def main():
    mobilenets_8hybrid()


if __name__ == '__main__':
    main()
