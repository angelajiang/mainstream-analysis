# -*- coding: utf8 -*-
import pprint as pp
import sys
import numpy as np
from PIL import Image
from matplotlib.pyplot import text
import matplotlib.pyplot as plt
import seaborn as sns
sys.path.append("scripts/util")
import plot_util


sns.set_style("white")

def visualize_deployment(files, objects, plot_dir, thumbnail):
    start = 50
    #end = 114

    # Use up and down arrow for hit/miss
    # settings = {'marker_hit': 6, 'marker_miss': 7, 'y_hit_m': .08, 'y_hit_c': .015, 'y_miss_c': .015, 'line': True}
    # settings = {'marker_hit': '^', 'marker_miss': 'v', 'y_hit_m': .08, 'y_hit_c': .015, 'line': True}
    settings = {'marker_hit': u'$\u2191$', 'marker_miss': 'v', 'y_hit_m': .08, 'y_hit_c': -.008, 'y_miss_c': .015, 'line': True}
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
                    xs1.append(frame_id)
                    ys1.append(i * settings['y_hit_m'] + settings['y_hit_c'])
                else:
                    xs2.append(frame_id)
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
            plt.axhline(y=i*settings['y_hit_m']+0.003, linestyle="--", color=obj["color"])

    train_front = 114
    plt.axvline(x= train_front, linestyle="--", color="black", alpha=0.8)
    plot_file = plot_dir + "/deploy-time-series.pdf"
    plt.title("Train detector with 9 apps", fontsize=20)

    plt.annotate("Train front",
                 xy=(train_front, -.1),
                 xytext=(-84, 12),
                 xycoords='data',
                 fontsize=15,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    # TODO(wonglkd): Fix this. Works with plt.show() but not with plt.savefig().
    im = Image.open(thumbnail)
    im.thumbnail((200, 200))
    plt.figimage(im, xo=40, yo=52, zorder=1)

    plt.xlim(start, max(xs1))
    plt.ylim(-.3, .15)
    plt.xlabel(u"Time (frames) →", fontsize=20)
    plt.xticks()
    plt.tick_params(axis='y', which='both', left='off', top='off', labelleft='off')
    # Fix legend order to match line appearance order
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles[::-1], labels[::-1], loc=4, fontsize=15, ncol=1, frameon=False)
    plt.savefig(plot_file, dpi=300)


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
