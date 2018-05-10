import os

def get_semester_dir():
    dirs = os.getcwd().split("/")
    idx = dirs.index("mainstream-analysis") + 1
    return "/".join(dirs[:idx + 1])

MAINSTREAM_DIR = os.path.join(os.path.dirname(__file__), "../../../mainstream")
SEMESTER_DIR = get_semester_dir()
