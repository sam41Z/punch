#!/usr/bin/env python3

import argparse

from datetime_parser import parse_time_span, parse_date
from add import add, add_sick
from hours import hours
from overtime import overtime
from remove import remove

def add_year_argument(parser):
    parser.add_argument('-y', '--year', type=int, choices=range(2021, 3000), metavar="2021+",
                        help="Year (2021 or later)")


def add_week_argument(parser):
    parser.add_argument('-w', '--week', type=int, choices=range(1, 52), metavar="[1-52]", help="Week number (1-52)")


def arguments_add(parser):
    parser.add_argument('time', type=parse_time_span, help="Time span like HH-HH or HH:mm-HH:mm")
    parser.add_argument('-d', '--date', type=parse_date, help="Date of the day logged as YYYY-MM-DD")
    parser.add_argument('-p', '--prefix', choices=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        help="Prefix of log line,describing the weekday.")


def arguments_sick(parser):
    parser.add_argument('-d', '--date', type=parse_date, help="Start date of sickness as YYYY-MM-DD")
    parser.add_argument('-p', '--prefix', choices=['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'],
                        help="Prefix of log line,describing the weekday.")


def arguments_remove(parser):
    parser.add_argument('-n', '--num', type=int, default=1, help='Number of lines to remove from the end')


def arguments_hours(parser):
    add_week_argument(parser)
    add_year_argument(parser)


def arguments_overtime(parser):
    parser.add_argument('week', type=int, choices=range(1, 52), metavar="[1-52]", help="Start week number (1-52)")


def parse_args():
    parser = argparse.ArgumentParser()
    sub_p = parser.add_subparsers(help="Type of operation", dest='operation')

    arguments_add(sub_p.add_parser('add', help="Add a new line"))
    arguments_remove(sub_p.add_parser('remove', help="Remove lines"))
    arguments_hours(sub_p.add_parser('hours', help="Calculate weekly hours"))
    arguments_overtime(sub_p.add_parser('overtime', help="Calculate overtime"))
    arguments_sick(sub_p.add_parser('sick', help="Add sick day"))

    return parser.parse_args()


if __name__ == '__main__':
    args = parse_args()
    if args.operation == 'remove':
        remove(args.num)
    elif args.operation == 'add':
        add(args.date, args.time, args.prefix)
    elif args.operation == 'sick':
        add_sick(args.date, args.prefix)
    elif args.operation == 'hours':
        hours(args.year, args.week)
    elif args.operation == 'overtime':
        overtime(args.week)

