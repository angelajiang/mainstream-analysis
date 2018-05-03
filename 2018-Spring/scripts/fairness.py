# Also an example of a script that would appear in a python notebook
import dataloaders
import plot


# Each function does one plot

def maxmin():
    .. = dataloaders.load_schedules(filename)
    # merge files if necessary

    # get some sort of dataframe-like thing to allow us to filter/etc by

    # sort/filter (dataframe like syntax)

    # aggregation (e.g. take the avg, take the mean)
    # error bars, if needed

    series = [.., ..]
    Series(schedules)

    plot.variants(series,
                  lambda s: s.mean_f1(),
                  lambda s: min(s.f1s),
                  lambda s: max(s.f1s),)





def heuristics():
    # agg by num_apps
    # agg by budget

# Metadata won't necessarirly propagate on DF filter etc
# https://stackoverflow.com/questions/14688306/adding-meta-information-metadata-to-pandas-dataframe