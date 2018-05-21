import sys
from scripts.scheduler import s7hybrid
from scripts.sharing import accuracies
from plotutils import contexts
contexts.use('paper')


def main():
    # Fig 4b
    accuracies.main()
    # Fig 7
    s7hybrid.main()


if __name__ == '__main__':
    main()
