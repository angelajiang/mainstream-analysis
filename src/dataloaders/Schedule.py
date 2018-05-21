import glob
import os
import sys
import warnings
from dl_constants import SCHEDULE_DIR
from dl_constants import MAINSTREAM_DIR 
from utils import mean
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/scheduler/types"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/scheduler"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "src/util"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "data"))
sys.path.append(os.path.join(MAINSTREAM_DIR, "data/mpackages"))
from scheduler_util import SharedStem


class Schedule(object):
    def __init__(self, fpses, num_frozens,
                 latency=None,
                 budget=None,
                 extras={},
                 apps_order='setup',
                 setup=None):
        # Calculate F1s using cost benefits loaded from setup file
        self._fpses = fpses
        self._frozens = num_frozens
        self._budget = budget
        self._latency = latency
        self._setup = setup
        self._extras = extras
        assert len(fpses) == len(num_frozens)

        if setup is not None:
            self._apps = setup.apps
            # Hack for exhaustive - use app order of configuration file.
            if apps_order == 'configurations':
                key_order = self._setup.cost_benefits.keys()
                apps_by_id = {app['app_id']: app for app in self._apps}
                self._apps = [apps_by_id[k] for k in key_order]

            self._f1s = [1. - x for x in self._metric("f1")]
            self._recalls = [1. - x for x in self._metric("fnr")]
            self._precisions = [1. - x for x in self._metric("fpr")]

            self._costs, self._objectives = [], []
            for app, num_frozen, fps in zip(self._apps, self._frozens, self._fpses):
                app_settings = self._setup.cost_benefits[app['app_id']]
                try:
                    cost, objective = app_settings[(num_frozen, fps)]
                except KeyError:
                    cost = self._setup.scheduler.get_cost(num_frozen, fps)
                    objective = self._setup.scheduler.get_metric(app, num_frozen, fps)
                self._costs.append(cost)
                self._objectives.append(objective)

            # TODO: Refactor to use method in mainstream Scheduler.py
            self._rel_accs = []
            self._accs = []
            for num_frozen, app in zip(self._frozens, self._apps):
                max_acc = max(app["accuracies"].values())
                cur_acc = app["accuracies"][num_frozen]
                self._accs.append(cur_acc)
                rel_acc = (max_acc - cur_acc) / max_acc
                self._rel_accs.append(rel_acc)

            if 'metric' in extras:
                assert abs(extras['metric'] - mean(self._objectives)) < 1e-5

            self._shared_stem()
            self._stem = SharedStem(self._shared_stem(), self._setup.scheduler.model)
            self._stem_cost = self._stem.cost

    def _metric(self, metric):
        metrics = []
        for app, num_frozen, fps in zip(self._apps, self._frozens, self._fpses):
            metrics.append(self._setup.scheduler._get_metric(app, num_frozen, fps, metric))
        return metrics

    def _shared_stem(self):
        max_fps = 0
        stem = {}
        for frozen, fps in sorted(zip(self.frozens, self.fpses), reverse=True):
            max_fps = max(max_fps, fps)
            if max_fps not in stem:
                stem[max_fps] = frozen
        return sorted((v, k) for k, v in stem.items())

    def __len__(self):
        return len(self._fpses)

    @property
    def num_apps(self):
        return len(self._fpses)

    @property
    def fpses(self):
        return self._fpses

    @property
    def frozens(self):
        return self._frozens

    @property
    def costs(self):
        return self._costs

    @property
    def objectives(self):
        return self._objectives

    @property
    def f1s(self):
        return self._f1s

    @property
    def recalls(self):
        return self._recalls

    @property
    def precisions(self):
        return self._precisions

    @property
    def rel_accs(self):
        return self._rel_accs

    @property
    def accs(self):
        return self._accs

    def extra(self, k):
        return self._extras[k]

    def mean_f1(self):
        return mean(self._f1s)

    def mean_recall(self):
        return mean(self._recalls)

    def mean_precision(self):
        return mean(self._precisions)

    @property
    def budget(self):
        return self._budget

    @property
    def latency(self):
        return self._latency

    @property
    def setup(self):
        return self._setup

    @property
    def stem(self):
        return self._stem

    @property
    def stem_cost(self):
        return self._stem_cost

    def __str__(self):
        return 'Schedule(f1={:g}, fpses={}, frozens={}, obj={})'.format(self.mean_f1(), self.fpses, self.frozens, self.objectives)

    def to_map(self, extras={}):
        dct = {
            'num_apps': self.num_apps,
            'budget': self._budget,
            'latency': self._latency,
            'f1': self.mean_f1(),
            'f1_min': min(self.f1s),
            'f1_max': max(self.f1s),
            'recall': self.mean_recall(),
            'precision': self.mean_precision(),
            'rel_acc': mean(self.rel_accs),
            'acc': mean(self.accs),
            'fps': mean(self.fpses),
        }
        dct.update(extras)
        return dct


def load(filename, setups={}, variant=None, **kwargs):
    assert variant in (None, 'v1+metrics', 'v1+cost')
    schedules = []
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip().split(',')
            # parse line
            extras = {}
            if filename.endswith(".v0"):
                raise NotImplementedError
            elif filename.endswith(".v1"):
                try:
                    idx = 0
                    setup_id = line[idx]
                    idx += 1
                    num_apps = int(line[idx])
                    idx += 1
                    num_cols = 1 + 2 + num_apps * 2 + 2
                    if variant == 'v1+metrics':
                        num_cols += 3
                    assert len(line) == num_cols, len(line)
                    extras['metric'] = float(line[idx])
                    idx += 1
                    frozens = map(int, line[idx:idx + num_apps])
                    idx += num_apps
                    try:
                        fpses = map(int, line[idx:idx + num_apps])
                    except ValueError:
                        fpses = map(float, line[idx:idx + num_apps])
                    idx += num_apps
                    budget = float(line[idx])
                    idx += 1
                    if variant == 'v1+cost':
                        extras['cost'] = float(line[idx])
                        latency_us = None
                    else:
                        latency_us = int(line[idx])
                    idx += 1
                    if variant == 'v1+metrics':
                        # If possible, verify that other stats match
                        f1_, recall_, precision_ = map(float, line[idx:idx + 3])
                        extras['f1'], extras['recall'], extras['precision'] = f1_, recall_, precision_
                        idx += 3
                    assert idx == len(line), idx
                except:
                    print "Offending line:", line
                    raise
            else:
                num_apps = int(line[0])
                assert len(line) == 1 + 3 + num_apps * 2
                # Note: f1_, if here, is incorrect as it is average of FNR/FPR
                fnr_, fpr_, acc_ = map(float, line[1:4])
                frozens = map(int, line[4:4 + num_apps])
                fpses = map(int, line[4 + num_apps:4 + num_apps * 2])
                # raise Exception("Unknown file format")
            if setup_id in setups:
                setup = setups[setup_id]
            else:
                warnings.warn("Setup " + setup_id + " not found")
                setup = None
            schedules.append(Schedule(fpses, frozens, budget=budget,
                                      latency=latency_us,
                                      setup=setup,
                                      extras=extras,
                                      **kwargs))
    return schedules


def load_dir(exp_id, suffix, workspace=SCHEDULE_DIR, **kwargs):
    schedules = []
    for filename in glob.glob(os.path.join(workspace.format(exp_id=exp_id), suffix)):
        schedules += load(filename, **kwargs)
    return schedules
