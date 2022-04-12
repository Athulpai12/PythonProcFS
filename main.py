import argparse

import SimpleProcParser


def main(pids):

    if pids:
        SimpleProcParser.print_stats_of_given_pids(pids)
    else:
        SimpleProcParser.print_process_info()


if __name__ == "__main__":
    parser = argparse.ArgumentParser("Prints the stat of processes")
    parser.add_argument('--pids', type=int, required=False, nargs='+')
    args = parser.parse_args()
    main(args.pids)
