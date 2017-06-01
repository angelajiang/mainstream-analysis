import matplotlib.pyplot as plt
import numpy as np

def plot_simultaneous(csv_file):
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')

def plot_partial(csv_file):
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')

def plot_shared(csv_file):
    with open(csv_file) as f:
        for line in f:
            vals = line.split(',')

if __name__ == "__main__":
    cmd = sys.argv[1]
    csv_file = sys.argv[2]
    if cmd == "simultaneous":
        plot_simulataneous(csv_file)
    elif cmd == "partial":
        plot_partial(csv_file)
    elif cmd == "shared":
        plot_partial(csv_file)
    else:
        print "cmd must be in {simultaneous, partial, shared}"

