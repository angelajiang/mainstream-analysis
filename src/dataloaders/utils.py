
def mean(xs):
    if not isinstance(xs, list):
        xs = list(xs)
    return sum(xs) / float(len(xs))


def hmean(xs):
    if not isinstance(xs, list):
        xs = list(xs)
    return len(xs) / sum(1. / x for x in xs)
