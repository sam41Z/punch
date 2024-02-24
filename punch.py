#!/usr/bin/env python

import argparse
from datetime import date, datetime

import migrate
import printer
from datetime_parser import parse_time_span
from hours import hours
from interactive import interactive_mode
from repository import Repository
from timerecord import add


def arguments_add(parser):
    parser.add_argument('time', type=parse_time_span, help="Time span like HH-HH or HH:mm-HH:mm")
    parser.add_argument('-p', '--prefix', choices=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        help="Prefix of log line, describing the weekday.")


def parse_args():
    parser = argparse.ArgumentParser()
    sub_p = parser.add_subparsers(help="Type of operation", dest='operation')
    arguments_add(sub_p.add_parser('add', help="Add a new log"))
    sub_p.add_parser('hours', help="Calculate weekly hours")
    migration_parser = sub_p.add_parser('migrate', help="Migrate data from old storage")
    migration_parser.add_argument('year', type=int, choices=range(2021, 3000), metavar="2021+",
                                  help="Year (2021 or later)")
    return parser.parse_args()


def add_args(args):
    today = date.today()
    starts_at, ends_at = args.time
    day = datetime.strptime("{0} {1} {2}".format(today.year, today.isocalendar().week, args.prefix),
                            "%Y %W %a").date() if args.prefix else today

    try:
        add(day, starts_at, ends_at)
    except ValueError as e:
        printer.print_error(str(e))


if __name__ == '__main__':
    args = parse_args()
    if args.operation is None:
        interactive_mode()
    elif args.operation == 'add':
        add_args(args)
    elif args.operation == 'hours':
        today = date.today()
        hours(today.year, today.isocalendar().week)
    elif args.operation == 'migrate':
        migrate.Migration(Repository.test()).migrate(args.year)
