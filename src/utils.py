from __future__ import print_function
import pickle
import datetime
from datetime import date
import inspect
import sys
import os
import matplotlib.pyplot as plt
from constants import PLOT_DIR


def save(group='', exp_id='', plot_id='', plot_dir=PLOT_DIR, **kwargs):
    if not os.path.exists(os.path.join(plot_dir, group, exp_id)):
        os.makedirs(os.path.join(plot_dir, group, exp_id))
    save_exact(os.path.join(plot_dir, group, exp_id, plot_id), **kwargs)


def save_exact(filename, pdf=True, png=False, **kwargs):
    rel_filename = filename.replace(os.getcwd() + "/", "")
    # set CreationDate to allow for deterministic PDFs to aid inclusion in git
    if pdf:
        plt.savefig(filename + ".pdf", metadata={'CreationDate': None}, **kwargs)
        print(rel_filename + ".pdf saved", file=sys.stderr)
    if png:
        plt.savefig(filename + ".png", metadata={'CreationDate': None}, dpi=72, **kwargs)
        print(rel_filename + ".png saved", file=sys.stderr)


def memoize(ext='.pkl', folder='_cache', stale_after=datetime.timedelta(days=1)):
    calling_file = inspect.getfile(sys._getframe(1))
    calling_filename = os.path.basename(calling_file).replace(".py", "")
    directory = os.path.join(os.path.dirname(calling_file), folder)

    def decorator(func):
        def wrapper(*args, **kwargs):
            parameters = ','.join(map(str, args)).replace(' ', '').replace("'", '')
            if len(parameters) > 0:
                parameters = "[{}]".format(parameters)
            filename = os.path.join(directory, calling_filename + parameters + ext)
            if (os.path.isfile(filename) and
                    date.fromtimestamp(os.path.getmtime(filename)) - date.today() <= stale_after):
                with open(filename) as f:
                    print("Loading from cache " + filename)
                    return pickle.load(f)
            else:
                if not os.path.isdir(directory):
                    os.mkdir(directory)
                with open(filename, 'wb') as f:
                    result = func(*args, **kwargs)
                    pickle.dump(result, f, pickle.HIGHEST_PROTOCOL)
                    return result

        return wrapper
    return decorator
