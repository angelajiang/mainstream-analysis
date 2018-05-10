import glob
import os


class Schedule(object):
    def __init__(self, fpses, num_frozens,
                 budget=None, setup=None):
        # Calculate F1s using cost benefits loaded from setup file
        self._fpses = fpses
        self._frozens = num_frozens
        self._budget = budget
        self._setup = setup

        self._f1s = self._metric("f1")
        self._recalls = [1. - x for x in self._metric("fnr")]
        self._precisions = [1. - x for x in self._metric("fpr")]

        self._costs, self._objectives = [], []
        for app, num_frozen, fps in zip(self._setup.apps, self._frozens, self._fpses):
            cost, objective = self._setup.cost_benefits[app.get_id()][(num_frozen, fps)]
            self._costs.append(cost)
            self._objectives.append(objective)

    def _metric(self, metric):
        metrics = []
        for app, num_frozen, fps in zip(self._setup.apps, self._frozens, self._fpses):
            metrics.append(self._setup.scheduler._get_metric(app.to_map(), num_frozen, fps, metric))
        return metrics

    def mean_f1(self):
        return sum(self._f1s) / float(len(self._f1s))

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
    def budget(self):
        return self._budget

    @property
    def setup(self):
        return self._setup


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
                fpses = map(int, line[idx:idx + num_apps])
                idx += num_apps
                budget, latency_us = line[idx:idx + 2]
                idx += 2
                # If possible, verify that other stats match
                f1_, recall_, precision_ = line[idx:idx + 3]
                idx += 3
                assert idx == len(line), idx
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


def load_dir(exp_id, suffix, workspace='output/scheduler/setups/{exp_id}/', **kwargs):
    schedules = []
    for filename in glob.glob(os.path.join(workspace.format(exp_id=exp_id), suffix)):
        schedules += load(filename, **kwargs)
    return schedules
