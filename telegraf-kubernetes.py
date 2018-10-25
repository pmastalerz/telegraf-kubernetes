#!/usr/bin/env python

import sys
import argparse
from kubernetes import Client, Parser


def __handle_cli(args):
    parser = argparse.ArgumentParser(
        description='Plugin for Telegraf for gathering statistics from Kubernetes')

    parser.add_argument(
        '--stats-url',
        help='Kubernetes stats URL',
        default="http://127.0.0.1:10255/stats/summary",
    )

    parser.add_argument(
        '--timeout',
        help='Timeout',
        default=5,
        type=int
    )

    return parser.parse_args(args)


def main(args):
    cli = __handle_cli(args)
    stats = Client(cli.stats_url, cli.timeout).get_stats()
    parsed = Parser().parse_stats(stats)

    sys.stdout.write(str(parsed))
    sys.stdout.write("\n")


if __name__ == '__main__':
    main(sys.argv[1:])
