import glob
import os
import pickle
import sys
from constants import MAINSTREAM_DIR
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/scheduler/types"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/scheduler"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/util"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "data"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "data/mpackages"))
import Setup
from Scheduler import Scheduler
import app_data_mobilenets as app_data


VERSION_SUFFIX = ".v1"

setup_dir = os.path.join(MAINSTREAM_DIR, "data/setups/{exp_id}")
config_filename = os.path.join(setup_dir, "setup/configuration.{setup_id}")
# setup_num_app_file = setup_dir + "/setups.{exp_id}-{num_apps}.v1"


def get_scheduler(setup):
    return Scheduler(None, setup.apps, setup.video_desc.to_map(), app_data.model_desc)


def get_cost_benefits(exp_id, setup):
    ret = {}
    with open(config_filename.format(exp_id=exp_id, setup_id=setup.uuid)) as f:
        for line in f:
            app_id, frozen, fps, cost, metric = line.split()
            if app_id not in ret:
                ret[app_id] = {}
            ret[app_id][(frozen, fps)] = (cost, metric)
    return ret


def load(exp_id):
    print "Loading setups...",
    setup_generator = Setup.SetupGenerator()
    all_setups = {}
    num_setups = 0
    setup_files = (setup_dir + "/setups.{exp_id}-*{version}.pickle").format(exp_id=exp_id, version=VERSION_SUFFIX)
    for pkl_filename in glob.glob(setup_files):
        setups = setup_generator.deserialize_setups(pkl_filename)
        for setup in setups:
            setup.scheduler = get_scheduler(setup)
            setup.cost_benefits = get_cost_benefits(exp_id, setup)
        all_setups.update({setup.uuid: setup for setup in setups})
        num_setups += len(setups)
        assert len(all_setups) == num_setups

    print "Done"
    return all_setups
