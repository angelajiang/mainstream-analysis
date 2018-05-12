import os
import sys
sys.path.append('../')
from constants import SEMESTER_DIR

MAINSTREAM_DIR = os.path.join(os.path.dirname(__file__), "../../../mainstream")
SCHEDULE_DIR = os.path.join(SEMESTER_DIR, 'output/scheduler/setups/{exp_id}/')
VERSION_SUFFIX = ".v1"
SETUP_DIR = os.path.join(MAINSTREAM_DIR, "data/setups/{exp_id}")
CONFIG_FILENAME = os.path.join(SETUP_DIR, "setup/configuration.{setup_id}")
SETUP_FILE_STR = "/setups.{exp_id}-*{version}.pickle"
