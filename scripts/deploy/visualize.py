# -*- coding: utf8 -*-
import sys
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
# mpl.style.use("classic")
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
import seaborn as sns
sys.path.append("scripts/util")
import plot_util

sns.set_style("white")


def visualize_deployment(files, objects, plot_dir, thumbnail):
    # TODO: Remove magic value of 20 (to compensate for startup time.)
    start = 50 + 20
    fps = 15.
    # end = 114

    # Use up and down arrow for hit/miss
    # settings = {'marker_hit': 6, 'marker_miss': 7, 'y_hit_m': .08, 'y_hit_c': .015, 'y_miss_c': .015, 'line': True}
    # settings = {'marker_hit': '^', 'marker_miss': 'v', 'y_hit_m': .08, 'y_hit_c': .015, 'line': True}
    settings = {'marker_hit': u'$\u2191$', 'marker_miss': 'v', 'y_hit_m': .08, 'y_hit_c': -.008 + .003, 'y_miss_c': .015 - .003, 'line': True}
    # settings = {'marker_hit': u'$\u2191$', 'marker_miss': u'$\u2193$', 'y_hit_m': .08, 'y_hit_c': -.008, 'y_miss_c': .016, 'line': True}
    # settings = {'marker_hit': '.', 'marker_miss': 'x', 'y_hit_m': .08, 'y_hit_c': .03, 'line': False}

    _, ax = plt.subplots(1)

    for i, (csv_file, obj) in enumerate(zip(files, objects)):
        xs1 = []
        xs2 = []
        ys1 = []
        ys2 = []
        with open(csv_file) as f:
            for line in f:
                vals = line.split(',')
                frame_id = int(vals[0])
                is_analyzed = int(vals[1])
                if is_analyzed == -1 or frame_id <= start:
                    continue
                if is_analyzed == 1:
                    xs1.append((frame_id - start) / fps)
                    ys1.append(i * settings['y_hit_m'] + settings['y_hit_c'])
                else:
                    xs2.append((frame_id - start) / fps)
                    ys2.append(i * settings['y_hit_m'] + settings['y_miss_c'])
        plt.scatter(xs1, ys1,
                    label=obj["label"] + " hit",
                    color=obj["color"],
                    s=70,
                    marker=settings['marker_hit'])
        plt.scatter(xs2, ys2,
                    label=obj["label"] + " miss",
                    color=obj["color"],
                    s=70,
                    marker=settings['marker_miss']),
        if settings['line']:
            plt.axhline(y=i * settings['y_hit_m'] + 0.003, linestyle="--", color=obj["color"])

    picture_loc = (104 - start) / float(fps)
    train_front = (114 - start) / float(fps)
    plt.axvline(x=train_front, linestyle="--", color="black", alpha=0.8)
    plot_file = plot_dir + "/deploy-time-series.pdf"
    # plt.title("Train detector with 9 concurrent apps", fontsize=20)

    plt.annotate("Smoke stack\nleaves view",
                 xy=(train_front, -.095),
                 xytext=(20, 12),
                 xycoords='data',
                 fontsize=15,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    im = Image.open(thumbnail)
    im.thumbnail((190, 190))

    imagebox = OffsetImage(im)
    imagebox.image.axes = ax

    ab = AnnotationBbox(imagebox, (picture_loc, 0),
                        xybox=(-30, -117),
                        xycoords='data',
                        boxcoords='offset points',
                        pad=0,
                        frameon=False,
                        arrowprops=dict(arrowstyle='->'))

    ax.add_artist(ab)
    # plt.figimage(im, xo=picture_loc * 72 - 150, yo=83 - 58, zorder=1)

    plt.xlim(0, max(xs1))
    plt.ylim(-.3, .15)
    plt.xlabel(u"Time elapsed (s)", fontsize=30)
    plt.xticks()
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)
    plt.tick_params(axis='y', which='both', left='off', top='off', labelleft='off')
    # Fix legend order to match line appearance order
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles[::-1], labels[::-1], loc=4, fontsize=15, ncol=1, frameon=False)
    plt.tight_layout()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)
    plt.savefig(plot_file)
    plt.clf()


if __name__ == "__main__":
    # Data created by mainstream analyze_deployment
    # Format: frame_id, is_analyzed
    f0 = "output/streamer/deploy/train/train2-10apps-nosharing"
    f1 = "output/streamer/deploy/train/train2-10apps-mainstream"
    f2 = "output/streamer/deploy/train/train2-10apps-maxsharing"
    thumbnail = "output/train-example.jpg"
    plot_dir = "plots/deploy"
    files = [f0, f1]
    objs = [plot_util.NO_SHARING, plot_util.MAINSTREAM]
    visualize_deployment(files, objs, plot_dir, thumbnail)
