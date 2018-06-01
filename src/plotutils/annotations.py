import matplotlib as mpl
import matplotlib.pyplot as plt


class Annotation(object):
    def __init__(self, pt, xy, name="", arrow_kwargs={}, **kwargs):
        self.pt = pt
        self.xy = xy
        self.name = name
        self.kwargs = kwargs
        self.arrow_kwargs = arrow_kwargs


def add_annotations(annotations,
                    series,
                    fmt_str='({name})',
                    extra={},
                    ax=None,
                    fontsize=1.):
    if ax is None:
        ax = plt.gca()
    # Transform {'fps': [series1, series2, series3], ...} to [{'fps': series1, ...}, ...]
    keys, vals = zip(*extra.items())
    extra = [zip(keys, row) for row in zip(*vals)]
    for s_annotations, s_, ss_extra in zip(annotations, series, extra):
        for annotation in s_annotations:
            x = s_.x[annotation.pt]
            y = s_.y[annotation.pt]
            fmt_vals = {'name': annotation.name}
            for k_extra, sss_extra in ss_extra:
                assert x == sss_extra.x[annotation.pt]
                fmt_vals[k_extra] = sss_extra.y[annotation.pt]

            common_args = dict(xy=(x, y),
                               xytext=annotation.xy,
                               xycoords='data',
                               fontsize=fontsize * mpl.rcParams['font.size'],
                               textcoords='offset points')
            # Annotation for arrow
            ax.annotate("",
                        arrowprops=dict(arrowstyle="->", **annotation.arrow_kwargs),
                        **common_args)
            # Annotation for text
            common_args.update(annotation.kwargs)
            ax.annotate(fmt_str.format(**fmt_vals),
                        **common_args)
