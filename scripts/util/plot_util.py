
from matplotlib import colors

MARKERS = ["o", "v", "D", "*", "p", "8", "h"]

# http://colorbrewer2.org/#type=diverging&scheme=Spectral&n=4
COLORLISTS = {3: [
                colors.colorConverter.to_rgb("#a6cee3"),
                colors.colorConverter.to_rgb("#1f78b4"),
                colors.colorConverter.to_rgb("#b2df8a"),
              ],
              4: [
                colors.colorConverter.to_rgb("#d53e4f"),
                colors.colorConverter.to_rgb("#fdae61"),
                colors.colorConverter.to_rgb("#abdda4"),
                colors.colorConverter.to_rgb("#2b83ba")
                ],
              5: [
                colors.colorConverter.to_rgb("#a6cee3"),
                colors.colorConverter.to_rgb("#1f78b4"),
                colors.colorConverter.to_rgb("#b2df8a"),
                colors.colorConverter.to_rgb("#33a02c"),
                colors.colorConverter.to_rgb("#fb9a99")
                ],
              8: [
                colors.colorConverter.to_rgb("#d53e4f"),
                colors.colorConverter.to_rgb("#f46d43"),
                colors.colorConverter.to_rgb("#fdae61"),
                colors.colorConverter.to_rgb("#fee08b"),
                colors.colorConverter.to_rgb("#e6f598"),
                colors.colorConverter.to_rgb("#abdda4"),
                colors.colorConverter.to_rgb("#66c2a5"),
                colors.colorConverter.to_rgb("#3288bd")
                ],
              12: [
                colors.colorConverter.to_rgb("#a6cee3"),
                colors.colorConverter.to_rgb("#1f78b4"),
                colors.colorConverter.to_rgb("#b2df8a"),
                colors.colorConverter.to_rgb("#33a02c"),
                colors.colorConverter.to_rgb("#fb9a99"),
                colors.colorConverter.to_rgb("#e31a1c"),
                colors.colorConverter.to_rgb("#fdbf6f"),
                colors.colorConverter.to_rgb("#ff7f00"),
                colors.colorConverter.to_rgb("#cab2d6"),
                colors.colorConverter.to_rgb("#6a3d9a"),
                colors.colorConverter.to_rgb("#ffff99"),
                colors.colorConverter.to_rgb("#b15928")
                ]
              }


COLORS = {"grey": colors.colorConverter.to_rgb("#4D4D4D"),
          "blue": colors.colorConverter.to_rgb("#2B83BA"),
          "orange": colors.colorConverter.to_rgb("#FDAE61"),
          "green": colors.colorConverter.to_rgb("#ABDDA4"),
          "seafoam": colors.colorConverter.to_rgb("#9DD192"),
          "pink": colors.colorConverter.to_rgb("#F2686D"),
          "brown": colors.colorConverter.to_rgb("#B2912F"),
          "purple": colors.colorConverter.to_rgb("#C988BB"),
          "yellow": colors.colorConverter.to_rgb("#DECF3F"),
          "red": colors.colorConverter.to_rgb("#d7191c"),
          "grey1": colors.colorConverter.to_rgb("#ffffff"),
          "grey2": colors.colorConverter.to_rgb("#f2f2f2"),
          "grey3": colors.colorConverter.to_rgb("#e6e6e6"),
          "grey4": colors.colorConverter.to_rgb("#d9d9d9"),
          "grey5": colors.colorConverter.to_rgb("#bfbfbf"),
          }

MAINSTREAM = {"color": COLORLISTS[8][0],
              "marker": "h",
              "pattern": "---",
              "label": "Mainstream"
              }

MAINSTREAM_VARIANT = {"color": COLORLISTS[4][1],
              "marker": "*",
              "pattern": "---",
              "label": "Mainstream-Variant",
              }

NO_SHARING = {"color": colors.colorConverter.to_rgb("#7fbf7b"),
              "marker": "<",
              "pattern": "\\\\",
              "label": "No Sharing"
              }

MAX_SHARING = {"color": COLORLISTS[8][7],
              "marker": "d",
              "pattern": "xxxxx",
              "label": "Max Sharing"
              }

def format_plot(xlabel, ylabel):
    import matplotlib.pyplot as plt
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.tick_params(axis='x', which='major', labelsize=28)
    plt.tick_params(axis='x', which='minor', labelsize=20)

    plt.legend(loc=0, fontsize=15)

    plt.xlabel(xlabel, fontsize=35)
    plt.ylabel(ylabel, fontsize=35)
    plt.tight_layout()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)


def format_plot_dual(ax1, ax2, xlabel, ylabel1, ylabel2):
    import matplotlib.pyplot as plt
    ax1.tick_params(axis='y', which='major', labelsize=23)
    ax1.tick_params(axis='y', which='minor', labelsize=20)
    ax1.tick_params(axis='x', which='major', labelsize=23)
    ax1.tick_params(axis='x', which='minor', labelsize=20)

    ax2.tick_params(axis='y', which='major', labelsize=23)
    ax2.tick_params(axis='y', which='minor', labelsize=20)
    ax2.tick_params(axis='x', which='major', labelsize=23)
    ax2.tick_params(axis='x', which='minor', labelsize=20)

    ax1.set_ylim(0, 1)

    ax1.set_xlabel(xlabel, fontsize=30)
    ax1.set_ylabel(ylabel1, fontsize=30)
    ax2.set_ylabel(ylabel2, fontsize=30)
    plt.tight_layout()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)

