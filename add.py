import argparse
import os
from datetime import datetime, date, timedelta
from rich import print
from rich.console import Group
from rich.panel import Panel
from files import get_file_path_by_date
from hours import logs


def day_prefix(arg_date, arg_prefix):
    if arg_date:
        day = arg_date
    else:
        day = date.today()

    if arg_prefix:
        prefix = arg_prefix
    else:
        prefix = day.strftime("%a")
    return day, prefix

def add(arg_date, arg_time, arg_prefix, arg_index):
    day, prefix = day_prefix(arg_date, arg_prefix)

    start_time, end_time = arg_time
    start = datetime.combine(day, start_time)
    end = datetime.combine(day, end_time)

    if end < start:
        msg = "End time ({}) is before start time ({})".format(end.strftime("%H:%M"), start.strftime("%H:%M"))
        raise argparse.ArgumentTypeError(msg)
    delta = end - start

    entry = '{} {} - {} {}'.format(prefix, start.strftime("%H:%M"), end.strftime("%H:%M"),
                                   ':'.join(str(delta).split(':')[:2]))
    filename = write(day, entry, arg_index)
    print_info(entry, filename)


def print_info(entry, filename):
    width = 50
    info = Group(
        Panel(entry, title="Added to file", width=width, title_align="left", style="spring_green1"),
        logs(filename, width)
    )
    print()
    print(Panel(info, title=":chart_increasing:", title_align="left", expand=False))


def write(day, entry, index):
    filename = get_file_path_by_date(day)
    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        if index is None:
            lines.append(entry + '\n')
        else:
            lines.insert(index, entry + '\n')
        file.writelines(lines)
    return filename


def add_sick(args_date, args_prefix, arg_index):
    day, prefix = day_prefix(args_date, args_prefix)
    delta = timedelta(hours=32) / 5
    print(delta)
    entry = '{} 🤒 {}'.format(prefix, ':'.join(str(delta).split(':')[:2]))
    filename = write(day, entry, arg_index)
    print_info(entry, filename)
