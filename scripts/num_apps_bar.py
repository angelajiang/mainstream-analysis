
import pprint as pp
import sys
import matplotlib
import numpy as np
import matplotlib.pyplot as plt

'''
matplotlib.use('Agg')
import matplotlib.pyplot as plt
plt.ioff()
'''

def plot(plot_file):
    labels = ["No Sharing", "Basic TL", "Mainstream"]
    ys = [2, 0, 7]
    width = 0.5
    ind = np.arange(len(labels))
    plt.title('W/in 98% accuracy, 5 FPS', fontsize=30)
    plt.bar(ind, ys, width=width, color="lightcoral")
    plt.tick_params(axis='y', which='major', labelsize=28)
    plt.tick_params(axis='y', which='minor', labelsize=20)
    plt.ylabel("Number of applications", fontsize=25)
    plt.xticks(ind + width / 2, labels, fontsize=20)
    plt.ylim(-1, 9)
    plt.savefig(plot_file)
    plt.clf()

    n_groups = 2
    ys_tl = (0, 0)
    ys_nosharing = (2, 1)
    ys_mainstream = (8, 8)
    fig, ax = plt.subplots()
    index = np.arange(n_groups)
    bar_width = 0.2

    rects1 = ax.bar(index, ys_nosharing, bar_width,
                    color='lightcoral',
                    label='No Sharing')
    rects2 = ax.bar(index + bar_width, ys_tl, bar_width,
                    color='mediumslateblue',
                    label='Basic TL')
    rects3 = ax.bar(index + (bar_width*2), ys_mainstream, bar_width,
                    color='lightgreen',
                    label='Mainstream')

    #ax.set_xticks((ind + bar_width * 2) / 2)
    print np.arange(2)
    xs = [i + (bar_width * (3 / 2)) for i in np.arange(2)]
    ax.set_xticks(xs)
    ax.set_xticklabels(('4 FPS', '8 FPS'))
    ax.tick_params(axis='both', which='major', labelsize=25)
    ax.tick_params(axis='both', which='minor', labelsize=20)
    ax.tick_params(axis='y', which='major', labelsize=25)
    ax.tick_params(axis='y', which='minor', labelsize=20)
    plt.ylabel('Number of applications', fontsize=28)
    plt.ylim(-1, 10)
    plt.title('Within 99% accuracy', fontsize=25)
    plt.legend(loc=0, fontsize=25)
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.show()
    plt.clf()

if __name__ == "__main__":
    plot("plots/num_apps_bar.pdf")
