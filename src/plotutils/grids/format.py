import matplotlib.pyplot as plt


def format(label_size=28):
    plt.tick_params(axis='y', which='major', labelsize=label_size)
    plt.tick_params(axis='y', which='minor', labelsize=label_size * .8)
    plt.tick_params(axis='x', which='major', labelsize=label_size)
    plt.tick_params(axis='x', which='minor', labelsize=label_size * .8)
    # plt.xlabel(xlabel, fontsize=label_size * 1.2)
    # plt.ylabel(ylabel, fontsize=label_size * 1.2)
    plt.tight_layout()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)


def format_dual(ax1, ax2):
    ax1.tick_params(axis='y', which='major', labelsize=23)
    ax1.tick_params(axis='y', which='minor', labelsize=20)
    ax1.tick_params(axis='x', which='major', labelsize=23)
    ax1.tick_params(axis='x', which='minor', labelsize=20)

    ax2.tick_params(axis='y', which='major', labelsize=23)
    ax2.tick_params(axis='y', which='minor', labelsize=20)
    ax2.tick_params(axis='x', which='major', labelsize=23)
    ax2.tick_params(axis='x', which='minor', labelsize=20)

    # ax1.set_xlabel(xlabel, fontsize=30)
    # ax1.set_ylabel(ylabel1, fontsize=30)
    # ax2.set_ylabel(ylabel2, fontsize=30)
    plt.tight_layout()
    plt.gca().xaxis.grid(True)
    plt.gca().yaxis.grid(True)
