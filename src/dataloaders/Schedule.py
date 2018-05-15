import glob
import os
from dl_constants import SCHEDULE_DIR
from utils import mean


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

        if 'metric' in extras:
            assert abs(extras['metric'] - mean(self._objectives)) < 1e-5

    def _metric(self, metric):
        metrics = []
        for app, num_frozen, fps in zip(self._apps, self._frozens, self._fpses):
            metrics.append(self._setup.scheduler._get_metric(app, num_frozen, fps, metric))
        return metrics

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

    def __str__(self):
        return 'Schedule(f1={:g}, fpses={}, frozens={}, obj={})'.format(self.mean_f1(), self.fpses, self.frozens, self.objectives)

    def to_map(self):
        return {
            'num_apps': self.num_apps,
            'budget': self._budget,
            'latency': self._latency,
            'f1': self.mean_f1(),
            'recall': self.mean_recall(),
            'precision': self.mean_precision(),
            'fps': mean(self.fpses),
        }


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
            schedules.append(Schedule(fpses, frozens, budget=budget,
                                      latency=latency_us,
                                      setup=setups[setup_id],
                                      extras=extras,
                                      **kwargs))
    return schedules


def load_dir(exp_id, suffix, workspace=SCHEDULE_DIR, **kwargs):
    schedules = []
    for filename in glob.glob(os.path.join(workspace.format(exp_id=exp_id), suffix)):
        schedules += load(filename, **kwargs)
    return schedules
