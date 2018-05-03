import numpy as np
import os
import pandas as pd
import sys


N_CURVES = 7
MAX_N_APPS = 10


def load_dfs(prefix):
    #dfs = [pd.read_csv(f, header=None) for f in filenames if os.path.isfile(f) and os.path.getsize(f) > 0]
    dfs = [pd.read_csv(sys.argv[1], header=None)]
    print dfs
    return proc_dfs(dfs)


def proc_dfs(df_all):
    df_all['No of applications'] = df_all[0]
    df_all['Avg FNR'] = df_all[1]
    df_all['Avg Rel Acc Loss'] = df_all[2]
    df_all['FNRs'] = df_all[3].str.split('_')
    df_all['Rel Acc Loss'] = df_all[4].str.split('_')

    baselines = {i: df_all[df_all[0] == 'mean={}'.format(i)] for i in range(N_CURVES)}
    baselines_fnr = {k: float(v['Avg FNR']) for k, v in baselines.items()}

    def aa(x):
        if not isinstance(x, list):
            x = [x]
        return map(float, x)

    for metric in ['Rel Acc Loss', 'FNR']:
        df_all[metric + 's'] = df_all[metric + 's'].fillna(df_all['Avg ' + metric]).apply(aa)

    # Normalise against baseline FNR.
    df_all['Curves'] = df_all[0].apply(lambda x: x.replace("mean=", "").split("_"))

    def norm(x):
        return [fnr / baselines_fnr[int(curve)]
                for curve, fnr in zip(x['Curves'], x['FNRs'])]

    def c_loss(x):
        return [fnr - baselines_fnr[int(curve)]
                for curve, fnr in zip(x['Curves'], x['FNRs'])]

    df_all['Normed FNRs'] = df_all.apply(norm, axis=1)
    df_all['Avg Normed FNR'] = df_all['Normed FNRs'].apply(np.mean)
    df_all['FNR Losss'] = df_all.apply(c_loss, axis=1)
    df_all['Avg FNR Loss'] = df_all['FNR Losss'].apply(np.mean)

    for metric in ['Rel Acc Loss', 'FNR', 'Normed FNR', 'FNR Loss']:
        df_all[metric + 's'] = df_all[metric + 's'].fillna(df_all['Avg ' + metric]).apply(aa)
        df_all['Min ' + metric] = df_all[metric + 's'].apply(min)
        df_all['Max ' + metric] = df_all[metric + 's'].apply(max)
        df_all['Max-Min ' + metric] = df_all[metric + 's'].apply(lambda x: max(x) - min(x))
        df_all['Max-Avg ' + metric] = df_all[metric + 's'].apply(lambda x: max(x) - sum(x) / float(len(x)))
        df_all['(Max-Min)/Max ' + metric] = df_all[metric + 's'].apply(lambda x: (max(x) - min(x)) / (max(x) + .01))

    return df_all, baselines_fnr


def filter_dfs(df, curves):
    return df[df['Curves'].apply(lambda x: len(set(map(int, x)) - set(curves)) == 0)]
