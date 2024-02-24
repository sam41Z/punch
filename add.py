import argparse
from datetime import datetime, date, timedelta

from rich import print
from rich.console import Group
from rich.panel import Panel

import repository
from files import get_file_path_by_date
from printer import get_record_table

from repository import create_record
from model import TimeRecord


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


def add(arg_date, arg_time, arg_prefix):
    day, prefix = day_prefix(arg_date, arg_prefix)

    start_time, end_time = arg_time
    start = datetime.combine(day, start_time)
    end = datetime.combine(day, end_time)

    new_record = TimeRecord(start, end)
    create_record(new_record)
    print_info(new_record)


def print_info(new_record: TimeRecord):
    year = new_record.started_at.year
    week = new_record.started_at.isocalendar().week
    entry = new_record.str_day() + " " + new_record.str_time() + " " + new_record.str_duration()
    records = repository.get_by_year_and_week(year, week)

    width = 50
    info = Group(
        Panel(entry, title="Added to file", width=width, title_align="left", style="spring_green1"),
        get_record_table(records, width)
    )
    print()
    print(Panel(info, title=":chart_increasing:", title_align="left", expand=False))


def write(day, entry, index):
    filename = get_file_path_by_date(day)
    try:
        with open(filename, 'r') as file:
            lines = file.readlines()
    except IOError:
        lines = []

    if index is None:
        lines.append(entry + '\n')
    else:
        lines.insert(index, entry + '\n')

    with open(filename, 'w') as file:
        file.writelines(lines)

    return filename
