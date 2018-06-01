from collections import OrderedDict
import hashlib
import glob
import os
import pickle
import sys
import warnings
from dl_constants import MAINSTREAM_DIR 
from dl_constants import VERSION_SUFFIX
from dl_constants import SETUP_DIR
from dl_constants import CONFIG_FILENAME
from dl_constants import SETUP_FILE_STR
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/scheduler/types"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/scheduler"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/util"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "data"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "data/mpackages"))
import Setup
from Scheduler import Scheduler
import app_data_mobilenets as app_data


def get_scheduler(setup, metric="f1"):
    # TODO: Make setup or something specify the metric.
    # TODO: Load layer costs from file instead of using app_data.model_desc.
    return Scheduler(metric, setup.apps, setup.video_desc.to_map(), app_data.model_desc)


def get_cost_benefits(exp_id, setup, setup_dir="", config_filename=CONFIG_FILENAME):
    # OrderedDict to aid schedule format hack for exhaustive - see schedule loader.
    ret = OrderedDict()
    config_filename = os.path.join(setup_dir, config_filename)
    with open(config_filename.format(exp_id=exp_id, setup_id=setup.uuid)) as f:
        for line in f:
            app_id, frozen, fps, cost, metric = line.split()
            frozen = int(frozen)
            fps = int(fps)
            cost = float(cost)
            metric = float(metric)
            if app_id not in ret:
                ret[app_id] = {}
            ret[app_id][(frozen, fps)] = (cost, metric)
    return ret


def _old_id(app):
    accuracies_str = ",".join([str(round(acc, 4)) for acc in app.accuracies.values()])
    prob_tnrs_str = ",".join([str(round(prob_tnr, 4)) for prob_tnr in app.prob_tnrs.values()])
    seed = str(app.architecture) + \
        accuracies_str + \
        prob_tnrs_str + \
        str(round(app.event_length_ms, 4)) + \
        str(round(app.event_frequency, 4)) + \
        str(round(app.correlation_coefficient, 4))

    hash_obj = hashlib.sha1(seed)
    app_uuid = hash_obj.hexdigest()[:8]
    return app.name + ":" + app_uuid


def load(exp_id, mainstream_dir=MAINSTREAM_DIR, setup_dir=SETUP_DIR, setup_file_str=SETUP_FILE_STR, version_suffix=VERSION_SUFFIX, legacy=None):
    print "Loading setups...",
    if legacy == 'InconsistentIds':
        print "Using InconsistentIds...",
    sys.stdout.flush()

    setup_generator = Setup.SetupGenerator()
    all_setups = {}
    setup_dir = os.path.join(mainstream_dir, setup_dir)
    setup_files = (setup_dir + setup_file_str).format(exp_id=exp_id, version=version_suffix)
    for pkl_filename in glob.glob(setup_files):
        setups = setup_generator.deserialize_setups(pkl_filename)
        for setup in setups:
            # For performance.
            setup._apps = setup.apps
            setup.apps = [app.to_map() for app in setup._apps]
            if legacy == 'InconsistentIds':
                for app, app_ in zip(setup.apps, setup._apps):
                    app['app_id'] = _old_id(app_)
            setup.scheduler = get_scheduler(setup)
            setup.cost_benefits = get_cost_benefits(exp_id, setup, setup_dir=setup_dir)
        for setup in setups:
            if setup.uuid in all_setups:
                warnings.warn("Duplicate setup " + setup.uuid) 
            all_setups[setup.uuid] = setup

    print "Done ({} loaded)".format(len(all_setups))
    return all_setups
