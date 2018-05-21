
def mean(xs):
    return sum(xs) / float(len(xs))


def hmean(xs):
    return len(xs) / sum(1. / x for x in xs)
