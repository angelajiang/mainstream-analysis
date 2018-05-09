# Also an example of a script that would appear in a python notebook
import dataloaders
import plot

# Each function does one plot

def f1_7hybrid():
    # TODO: Have some sort of namespacing
    # Make it work regardless of ...
    # Some sort of directory matching? Use glob?
    setups = dataloaders.load_setups("050318")
    dataloaders.load_schedule("output/scheduler/setups/050318/greedy.mainstream.sim.50.050318-2.v1", setups=setups)

if __name__ == '__main__':
    f1_7hybrid()

# def maxmin():
#     .. = dataloaders.load_schedules(filename)
#     # merge files if necessary

#     # get some sort of dataframe-like thing to allow us to filter/etc by

#     # sort/filter (dataframe like syntax)

#     # aggregation (e.g. take the avg, take the mean)
#     # error bars, if needed

#     series = [.., ..]
#     Series(schedules)

#     plot.variants(series,
#                   lambda s: s.mean_f1(),
#                   lambda s: min(s.f1s),
#                   lambda s: max(s.f1s),)





# def heuristics():
#     # agg by num_apps
#     # agg by budget

# # Metadata won't necessarirly propagate on DF filter etc
# # https://stackoverflow.com/questions/14688306/adding-meta-information-metadata-to-pandas-dataframe