# -*- coding: utf8 -*-
import os
import sys
from PIL import Image
import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.offsetbox import OffsetImage, AnnotationBbox
from mpl_toolkits.axes_grid.axislines import SubplotZero
sys.path.append("scripts/util")
import plot_util

# Restore some aspects of matplotlib 1
mpl.rcParams['figure.figsize'] = [8.0, 6.0]
mpl.rcParams['figure.dpi'] = 80
mpl.rcParams['savefig.dpi'] = 100

mpl.rcParams['font.size'] = 12
mpl.rcParams['legend.fontsize'] = 'large'
mpl.rcParams['figure.titlesize'] = 'medium'
mpl.rcParams['pdf.fonttype'] = 42
mpl.rcParams['ps.fonttype'] = 42
mpl.rcParams.update({
    'mathtext.fontset': 'custom',
    'mathtext.rm': 'Bitstream Vera Sans',
    'mathtext.it': 'Bitstream Vera Sans:italic',
    'mathtext.bf': 'Bitstream Vera Sans:bold',    
})

sizes = {
    'label': 30,
    'legend': 20,
}

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
    settings['y_offset'] = .03

    fig = plt.figure(1)
    ax = SubplotZero(fig, 111)
    fig.add_subplot(ax)

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
                    ys1.append(i * settings['y_hit_m'] + settings['y_hit_c'] + settings['y_offset'])
                else:
                    xs2.append((frame_id - start) / fps)
                    ys2.append(i * settings['y_hit_m'] + settings['y_miss_c'] + settings['y_offset'])
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
            y = i * settings['y_hit_m'] + 0.003 + settings['y_offset']
            # plt.axhline(y=y, lw=2, linestyle=":", color=obj["color"])
            plt.arrow(x=0, y=y, dx=13.6, dy=0, head_width=0.01, head_length=0.2, facecolor='black', alpha=.7, ls=":", color=obj["color"])

    picture_loc = (104 - start) / float(fps)
    train_front = (114 - start) / float(fps)
    plt.axvline(x=train_front, linestyle="--", color="black", alpha=0.8, ymin=.10 + .2)
    plot_file = plot_dir + "/deploy-time-series.pdf"
    # plt.title("Train detector with 9 concurrent apps", fontsize=20)

    ax.yaxis.set_visible(False)
    ax.spines['right'].set_visible(False)
    ax.spines['left'].set_visible(False)
    ax.spines['top'].set_visible(False)

    for direction in ["xzero"]:
        ax_ = ax.axis[direction]
        ax_.set_axisline_style("-|>")
        ax_.set_visible(True)
        ax_.major_ticks.set_ticksize(10)
        ax_.label.set_fontsize(20)
        ax_.major_ticklabels.set(fontsize=20)
        ax_.major_ticks.set_tick_out(True)

    for direction in ["left", "right", "bottom", "top"]:
        ax.axis[direction].set_visible(False)

    xybox = [-30, -160-55]
    extent = [0, .6, 7.9, 6]
    legend_bbox = [1.05, .08]
    smokestack_xy = [train_front, -.095 - .1]
    smokestack_text = [20, 30]

    # To put it at the side
    xybox[0] += -110
    xybox[1] += 170
    extent[0] += -1.3
    extent[1] += 1.1
    legend_bbox[1] += .22
    smokestack_xy[1] += .07
    smokestack_text[0] -= 200
    smokestack_text[1] -= 30

    plt.annotate("Smoke stack\nleaves view",
                 xy=smokestack_xy,
                 xytext=smokestack_text,
                 xycoords='data',
                 fontsize=20,
                 textcoords='offset points',
                 arrowprops=dict(arrowstyle="->"))

    im = Image.open(thumbnail)
    im.thumbnail((185, 185))

    imagebox = OffsetImage(im)
    imagebox.image.axes = ax

    ab = AnnotationBbox(imagebox, (picture_loc, settings['y_hit_m'] + settings['y_hit_c'] + settings['y_offset'] - .004),
                        xybox=xybox,
                        xycoords='data',
                        boxcoords='offset points',
                        pad=0,
                        frameon=False,
                        arrowprops=dict(arrowstyle='->'))

    ax.add_artist(ab)
    # plt.figimage(im, xo=picture_loc * 72 - 150, yo=83 - 58, zorder=1)

    plt.xlim(0, max(xs1) + .5)
    plt.ylim(-.3, .15)
    plt.xlabel(u"Time elapsed (s)", fontsize=sizes['label'])
    plt.xticks(range(0, int(max(xs1)), 4))
    # plt.tick_params(axis='y', which='major', labelsize=28)
    # plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=35)
    plt.tick_params(axis='x', which='minor', labelsize=30)
    plt.tick_params(axis='y', which='both', left=False, top=False, labelleft=False)
    # Fix legend order to match line appearance order
    handles, labels = ax.get_legend_handles_labels()
    plt.legend(handles[::-1], labels[::-1], loc=4, fontsize=sizes['legend'], ncol=2, columnspacing=0, handletextpad=0, frameon=False, bbox_to_anchor=legend_bbox)
    plt.tight_layout(rect=[0, 0, .97, 1])
    plt.savefig(plot_file, metadata={'CreationDate': None}, bbox_inches=mpl.transforms.Bbox.from_extents(extent))
    plt.clf()


if __name__ == "__main__":
    # Data created by mainstream analyze_deployment
    # Format: frame_id, is_analyzed
    f0 = "output/streamer/deploy/train/train2-10apps-nosharing"
    f1 = "output/streamer/deploy/train/train2-10apps-mainstream"
    f2 = "output/streamer/deploy/train/train2-10apps-maxsharing"
    thumbnail = "output/train-example.jpg"
    plot_dir = "plots/deploy"
    if not os.path.exists(plot_dir):
        os.makedirs(plot_dir)
    files = [f0, f1]
    objs = [plot_util.NO_SHARING, plot_util.MAINSTREAM]
    visualize_deployment(files, objs, plot_dir, thumbnail)
