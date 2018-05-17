import sys
from plotutils import contexts
contexts.use('paper')
sys.path.append('scripts/scheduler')
import 7hybrid


def main():
    # Fig 7
    7hybrid.main()


if __name__ == '__main__':
    main()