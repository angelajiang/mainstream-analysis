import subprocess
from scripts.scheduler import *
from scripts.sharing import *
from scripts import *
from plotutils import contexts
contexts.use('paper')


def main():
    # Fig 4a
    #throughput.main()
    # Fig 4b
    accuracies.main()
    # Fig 5
    #dependence.main()
    # Fig 6, 7
    #s7hybrid.main()
    # Fig 8
    #Jcorrelations.main()
    # Fig 9
    #x_voting.main()
    # Fig 10
    #subprocess.check_call('python scripts/deploy/visualize.py', cwd='../pre-2018-Spring', shell=True)


if __name__ == '__main__':
    main()
