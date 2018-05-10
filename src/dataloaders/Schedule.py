import glob
import os
from constants import SEMESTER_DIR
from utils import mean


class Schedule(object):
    def __init__(self, fpses, num_frozens,
                 budget=None, setup=None):
        # Calculate F1s using cost benefits loaded from setup file
        self._fpses = fpses
        self._frozens = num_frozens
        self._budget = budget
        self._setup = setup

        assert len(fpses) == len(num_frozens)

        self._f1s = self._metric("f1")
        self._recalls = [1. - x for x in self._metric("fnr")]
        self._precisions = [1. - x for x in self._metric("fpr")]

        self._costs, self._objectives = [], []
        for app, num_frozen, fps in zip(self._setup.apps, self._frozens, self._fpses):
            try:
                cost, objective = self._setup.cost_benefits[app.get_id()][(num_frozen, fps)]
            except KeyError:
                cost = self._setup.scheduler.get_cost(num_frozen, fps)
                objective = self._setup.scheduler.get_metric(app.to_map(), num_frozen, fps)
            self._costs.append(cost)
            self._objectives.append(objective)

    def _metric(self, metric):
        metrics = []
        for app, num_frozen, fps in zip(self._setup.apps, self._frozens, self._fpses):
            metrics.append(self._setup.scheduler._get_metric(app.to_map(), num_frozen, fps, metric))
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
        return self.frozens

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
    def setup(self):
        return self._setup

    def to_map(self):
        return {
            'num_apps': self.num_apps,
            'budget': self._budget,
            'mean_f1': self.mean_f1(),
            'mean_recall': self.mean_recall(),
            'mean_precision': self.mean_precision(),
        }


def load(filename, setups={}):
    schedules = []
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            line = line.strip().split(',')
            # parse line
            if filename.endswith(".v0"):
                raise NotImplementedError
            elif filename.endswith(".v1"):
                try:
                    idx = 0
                    setup_id = line[idx]
                    idx += 1
                    num_apps = int(line[idx])
                    idx += 1
                    assert len(line) == 1 + 2 + num_apps * 2 + 2 + 3, len(line)
                    metric = float(line[idx])
                    idx += 1
                    frozens = map(int, line[idx:idx + num_apps])
                    idx += num_apps
                    try:
                        fpses = map(int, line[idx:idx + num_apps])
                    except ValueError:
                        fpses = map(float, line[idx:idx + num_apps])
                    idx += num_apps
                    budget, latency_us = line[idx:idx + 2]
                    budget = float(budget)
                    latency_us = int(latency_us)
                    idx += 2
                    # If possible, verify that other stats match
                    f1_, recall_, precision_ = map(float, line[idx:idx + 3])
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
                                      setup=setups[setup_id]))
    return schedules


def load_dir(exp_id, suffix, workspace=os.path.join(SEMESTER_DIR, 'output/scheduler/setups/{exp_id}/'), **kwargs):
    schedules = []
    for filename in glob.glob(os.path.join(workspace.format(exp_id=exp_id), suffix)):
        schedules += load(filename, **kwargs)
    return schedules
