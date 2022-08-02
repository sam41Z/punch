import argparse
from datetime import datetime


def parse_time(s):
    try:
        return datetime.strptime(s, "%H:%M").time()
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%H").time()
    except ValueError:
        msg = "not a valid time: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_time_span(s):
    try:
        times = s.split('-')
        if len(times) != 2:
            raise ValueError
        start = times[0]
        end = times[1]
        return parse_time(start), parse_time(end)
    except ValueError:
        msg = "not a valid time span: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)


def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "not a valid date: {0!r}".format(s)
        raise argparse.ArgumentTypeError(msg)