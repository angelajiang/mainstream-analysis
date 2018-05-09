

class Schedule(object):
    def __init__(self, fpses, num_frozens,
                 budget=None, setup=None):
        # Calculate F1s using cost benefits loaded from setup file
        self._fpses = fpses
        self._num_frozens = num_frozens
        self._budget = budget
        self._setup = setup

        metric = "f1"
        for app, num_frozen, fps in zip(self._setup.apps, num_frozens, fpses):
            setup.scheduler._get_metric(app.to_map(), num_frozen, fps, metric)
        # cost, benefits
        # F1s

        print(setup)

    def mean_f1(self):
        pass

    def f1s(self):
        pass

    def budget(self):
        return self._budget

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
                pass
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
