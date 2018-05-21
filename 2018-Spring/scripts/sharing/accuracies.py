import dataloaders
import plot
import plotutils
from plotutils import grids
from plotutils import legends
from utils import save


def mpackages2series(mpackages):
    # TODO: Markers, colors (e.g. red car should be red)
    # TODO: Arrange by value [last value, majority highest]
    # TODO: Normalize x value to be percent
    return [plotutils.Series(series=p_.accuracies.acc,
                             plotstyle={'label': p_.label},
                             plotparams=plotutils.LINEGROUPS['fg'])
            for p_ in mpackages]


def _plot(packages):
    return plot.variants(mpackages2series(packages),
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
