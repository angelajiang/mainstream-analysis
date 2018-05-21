from .colors import COLORLISTS, COLORS
from matplotlib import colors as mpl_colors

MARKERS = ["o", "v", "D", "*", "p", "8", "h", "x", "x", "d", "|", "2", "3", "4"]
MARKERSIZES = [4] * len(MARKERS)
# * is small compared to the others.
MARKERSIZES[3] *= 1.5

CAPSIZES = [10, 6, 3, 8, 4]

LINEGROUPS = {
    'fg': dict(lw=2, markersize=4, marker='.'),
    'fg-e': dict(lw=2, markersize=4, markeredgewidth=1),
    'bg': dict(lw=1, markersize=4, alpha=0.7, linestyle='--'),
    'bg-e': dict(lw=1, markersize=4, alpha=0.7, linestyle='--', markeredgewidth=1),
}


MAINSTREAM = {
    "color": COLORLISTS[8][0],
    "marker": "h",
    "marker_alt": "s",
    "pattern": "---",
    "label": "Mainstream"
}

MAINSTREAM_VARIANT = {
    "color": COLORLISTS[4][1],
    "marker": "*",
    "pattern": "---",
    "label": "Mainstream-Variant",
}

NO_SHARING = {
    "color": mpl_colors.colorConverter.to_rgb("#7fbf7b"),
    "marker": "<",
    "marker_alt": ">",
    "pattern": "\\\\",
    "label": "No Sharing",
}

MAX_SHARING = {
    "color": COLORLISTS[8][7],
    "marker": "d",
    "marker_alt": "D",
    "pattern": "xxxxx",
    "label": "Max Sharing",
}

GREEDY = {
    "color": COLORS["orange"],
    "marker": "h",
    "label": "Greedy",
}

EXHAUSTIVE = {
    "color": COLORS["red"],
    "marker": "*",
    "label": "Exhaustive",
}

STEMS = {
    "color": COLORS["blue"],
    "marker": "<",
    "label": "Stems",
}

SERIES = {
    # Sharing
    'mainstream': MAINSTREAM,
    'maxsharing': MAX_SHARING,
    'nosharing': NO_SHARING,

    # Scheduler
    'greedy': GREEDY,
    'exhaustive': EXHAUSTIVE,
    'stems_cpp': STEMS,
}

SERIES_ALT = {}
for k, v in SERIES.items():
    v = dict(v)
    if 'marker_alt' in v:
        v['marker'] = v.pop('marker_alt')
    SERIES_ALT[k] = v
