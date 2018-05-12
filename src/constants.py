import os


def get_semester_dir():
    dirs = os.getcwd().split("/")
    idx = dirs.index("mainstream-analysis") + 1
    return "/".join(dirs[:idx + 1])

SEMESTER_DIR = get_semester_dir()
PLOT_DIR = os.path.join(SEMESTER_DIR, 'plots')
