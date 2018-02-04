import numpy as np
from scipy.stats import hmean
import subprocess
import glob


def get_recall_data(csv_file, version):
    # Version 0: num_apps,fnr,acc_loss,fps_list...,frozen_list...
    # Version 1: num_apps,fnr,fpr,acc_loss,fps_list...,frozen_list...
    metrics = {}
    fpses = {}
    acc_losses = {}
    xs = []
    ys = []
    errs = []
    as1 = []
    as2 = []
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            if vals[0].isdigit():
                num_apps = int(vals[0])
            else:
                num_apps = len(vals[0].split("_"))

            if version == 0:  # NSDI
                acc_loss = round(float(vals[2]),2)
                fps_start = num_apps + 4
                fps_end = (2 *num_apps) + 3
                fps_list = [float(v) for v in vals[fps_start:fps_end]]
                average_fps = round(np.average(fps_list),2)
            if version == 1:
                acc_loss = round(float(vals[3]),2)
                fps_start = num_apps + 5
                fps_end = (2 *num_apps) + 4
                fps_list = [float(v) for v in vals[fps_start:fps_end]]
                average_fps = round(np.average(fps_list), 2)

            if num_apps not in metrics.keys():
                xs.append(num_apps)
                metrics[num_apps] = []
                acc_losses[num_apps] = []
                fpses[num_apps] = []

            fnr = float(vals[1])
            metrics[num_apps].append(1 - fnr)
            acc_losses[num_apps].append(acc_loss)
            fpses[num_apps].append(average_fps)

    for x in xs:
        ys.append(np.average(metrics[x]))
        errs.append(np.std(metrics[x]))
        as1.append(round(np.average(acc_losses[x]), 2))
        as2.append(round(np.average(fpses[x]), 2))
    return xs, ys, errs, as1, as2


def get_precision_data(csv_file):
    # Assumes Version 1
    # Version 1: num_apps,fnr,fpr,acc_loss,fps_list...,frozen_list...
    metrics = {}
    fpses = {}
    acc_losses = {}
    xs = []
    ys = []
    errs = []
    as1 = []
    as2 = []

    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            if vals[0].isdigit():
                num_apps = int(vals[0])
            else:
                print "Interpreting as combs"
                num_apps = len(vals[0].split("_"))
            acc_loss = round(float(vals[3]),2)
            fps_start = num_apps + 5
            fps_end = (2 *num_apps) + 4
            fps_list = [float(v) for v in vals[fps_start:fps_end]]
            average_fps = round(np.average(fps_list), 2)

            if num_apps not in metrics.keys():
                xs.append(num_apps)
                metrics[num_apps] = []
                acc_losses[num_apps] = []
                fpses[num_apps] = []

            fnr = float(vals[1])
            fpr = float(vals[2])
            metrics[num_apps].append(1 - fpr)
            acc_losses[num_apps].append(acc_loss)
            fpses[num_apps].append(average_fps)

    for x in xs:
        ys.append(np.average(metrics[x]))
        errs.append(np.std(metrics[x]))
        as1.append(round(np.average(acc_losses[x]), 2))
        as2.append(round(np.average(fpses[x]), 2))
    return xs, ys, errs, as1, as2


def get_f1_data(csv_file):
    # Assumes Version 1
    # Version 1: num_apps,fnr,fpr,acc_loss,fps_list...,frozen_list...
    metrics = {}
    xs = []
    ys = []
    errs = []
    avg_losses = []
    avg_fpses = []
    acc_losses = {}
    fpses = {}

    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')
            if vals[0].isdigit():
                num_apps = int(vals[0])
            else:
                print "Interpreting as combs"
                num_apps = len(vals[0].split("_"))
            # acc_loss = round(float(vals[3]),2)
            fps_start = num_apps + 4
            fps_end = (2 *num_apps) + 4
            fps_list = [float(v) for v in vals[fps_start:fps_end]]
            average_fps = round(np.average(fps_list), 2)

            if num_apps not in metrics.keys():
                xs.append(num_apps)
                metrics[num_apps] = []
                acc_losses[num_apps] = []
                fpses[num_apps] = []

            fnr = float(vals[1])
            fpr = float(vals[2])
            if fpr == 1:
                fpr = 0
                print "WARNING: No false positives. Set precision to 0"
            f1 = hmean([1 - float(fnr), 1 - float(fpr)])
            metrics[num_apps].append(f1)
            # acc_losses[num_apps].append(acc_loss)
            fpses[num_apps].append(average_fps)

    for x in xs:
        ys.append(np.average(metrics[x]))
        errs.append(np.std(metrics[x]))
        avg_losses.append(round(np.average(acc_losses[x]), 2))
        avg_fpses.append(round(np.average(fpses[x]), 2))

    return xs, ys, errs, avg_losses, avg_fpses


def collect_comb_csvs(comb_files_loc):
    """cat files-*- > files-combined- """
    new_file_name = comb_files_loc.replace("-*-", "_combined-")
    files = sorted(glob.glob(comb_files_loc), key=lambda x: int(x.split('-')[-3]))
    with open(new_file_name, "w") as f:
        subprocess.call(["cat"] + files, stdout=f)
    return new_file_name
