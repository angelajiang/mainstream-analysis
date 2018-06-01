import csv
from collections import OrderedDict
import pandas as pd

# TODO: Do namespacing the way it is done in other dataloaders.
# csv_file = "../pre-2018-Spring/" + "output/streamer/throughput/inception/flow_control/multi-app"


def op_to_layer(op_full):
    tensor_name = (op_full.split(":"))[0]
    layer = tensor_name.split("/")[0]
    return layer


def layer_idx(filename):
    """Assumes that layers in file are ordered."""
    layers = OrderedDict()
    with open(filename) as f:
        for line in csv.reader(f):
            layer = op_to_layer(line[0])
            if layer not in layers:
                layers[layer] = len(layers)
    return layers


def load(filename):
    # format: layerOp, num_NN, base, task1, task2, ..
    rows = []
    layer_to_id = layer_idx(filename)
    with open(filename) as f:
        for line in csv.reader(f):
            row = {
                'op_full': line[0],
                'layer': op_to_layer(line[0]),
                'layer_id': layer_to_id[op_to_layer(line[0])],
                'num_NNs': int(line[1]),
                'base': float(line[2]),
                'tasks': map(float, line[3:]),
                'num_tasks': len(line[3:]),
            }
            if len(row['tasks']) != 0:
                row['task_avg'] = sum(row['tasks']) / len(row['tasks'])
                assert len(row['tasks']) == row['num_NNs']
            else:
                row['task_avg'] = None
            rows.append(row)
    return pd.DataFrame(rows)


def as_throughput(df):
    df['task_avg'] = df['task_avg'].fillna(df['base'])
    mask = df['base'] == 0
    df.ix[mask, 'base'] = df['task_avg'].where(mask)
    return df
