
class Schedule(object):
    def __init__(self, fpses, num_frozens,
                 budget=None, setup=None):
        # Calculate F1s using cost benefits loaded from setup file
        pass

    def mean_f1(self):
        pass

    def f1s(self):
        pass

    def budget(self):
        return self._budget

    def setup(self):
        return self._setup


# TODO: detect version

def load(filename):
    schedules = []
    with open(filename) as f:
        for line in f:
            if line.startswith('#'):
                continue
            # parse line
            fpses, frozens, setup, ... = ...
            schedules.append(Schedule(fpses, frozens, budget))
            # If possible, verify that other stats match
