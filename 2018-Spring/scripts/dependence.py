import plot
from plotutils import agg2series
from plotutils import grids
from plotutils import styles
from utils import save

# For dataloader
import os
import pandas as pd


OUTPUT_DIR = "../pre-2018-Spring/output"
CORRELATIONS_DIR = "mainstream/frame-rate"


def load(filename, corr):
    df = pd.read_csv(filename, names=['stride', 'recall'])
    df['sample_rate'] = 1. / df['stride']
    df['correlation'] = corr
    return df


def load_dataset(dataset,
                 output_dir=OUTPUT_DIR,
                 correlations_dir=CORRELATIONS_DIR):
    corr_types = ["dependent-whole",
                  "independent-whole",
                  "empirical-temporal",
                  "empirical-random",
                  "correlation"]
    dfs = []
    for corr in corr_types:
        filename = os.path.join(output_dir, correlations_dir, dataset + "-" + corr)
        if os.path.isfile(filename):
            dfs.append(load(filename, corr))
    return pd.concat(dfs)


def sample_rate_recall(dataset, dataset_prefix, event_lengths):
    df = load_dataset(dataset_prefix)
    grouped = df.groupby(['correlation', 'sample_rate'])
    names = ["independent-whole",
             "empirical-temporal" if "empirical-temporal" in df['correlation'].values else "empirical-random",
             "correlation",
             "dependent-whole"]
    plotstyles = [
        {'label': "Fully Independent", 'color': 'blue'},
        {'label': "Profiled", 'color': 'green'},
        {'label': "Mainstream Prediction", 'color': styles.MAINSTREAM['color']},
        {'label': "Fully Dependent", 'color': 'turquoise'},
    ]
    series = agg2series(grouped['recall'].mean(),
                        names=names,
                        plotstyles=plotstyles,
                        plotparams=dict(lw=2))
    ax = plot.variants(series,
                       xgrid=grids.x.sample_rate,
                       ygrid=grids.y.recall_zoomed)
    # Add event lengths
    for length in event_lengths:
        ax.axvline(x=1. / length, linestyle="--", color="black", alpha=0.3, lw=1)
    save(group="correlations", plot_id='recall-samplerate-' + dataset)


def main():
    event_lengths = [286, 77, 92, 437, 274, 255, 251, 153]
    sample_rate_recall("train", "no-afn/train/v2/trains-313", event_lengths)

    event_lengths = [49, 9, 42, 52, 77, 18, 90, 9, 76, 111, 149, 66, 34, 30, 77, 31, 28, 31, 8, 2, 151, 44, 33, 44, 30, 40, 38, 115, 55, 23, 257, 5, 32, 1681, 103, 18, 110, 66, 76, 86, 124, 39, 74, 29, 71, 40, 63, 23, 81]
    sample_rate_recall("pedestrian", "pedestrian/atrium/atrium-mobilenets-84", event_lengths)


if __name__ == '__main__':
    main()
