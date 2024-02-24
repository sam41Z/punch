import argparse
import os
from datetime import datetime, date
from rich import print
from rich.console import Group
from rich.panel import Panel
from files import get_file_path_by_date
from hours import logs


def add(arg_date, arg_time, arg_prefix):
    if arg_date:
        day = arg_date
    else:
        day = date.today()

    start_time, end_time = arg_time
    start = datetime.combine(day, start_time)
    end = datetime.combine(day, end_time)

    if end < start:
        msg = "End time ({}) is before start time ({})".format(end.strftime("%H:%M"), start.strftime("%H:%M"))
        raise argparse.ArgumentTypeError(msg)
    delta = end - start
    if arg_prefix:
        day = arg_prefix
    else:
        day = start.strftime("%a")
    entry = '{} {} - {} {}'.format(day, start.strftime("%H:%M"), end.strftime("%H:%M"),
                                   ':'.join(str(delta).split(':')[:2]))
    filename = get_file_path_by_date(start.date())
    with open(filename, 'a') as file:
        file.write(entry + '\n')

    width = 50
    info = Group(
        Panel(entry, title="Appended to file", width=width, title_align="left", style="spring_green1"),
        logs(filename, width)
    )
    print(Panel(info, title=":chart_increasing:", title_align="left", expand=False))
