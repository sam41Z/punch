import math, repository
from datetime import datetime, timedelta, date, time
from functools import reduce

from rich import print, box
from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TaskProgressColumn
from rich.style import Style
from rich.table import Table

from holidays import weekly_and_holidays
import repository


def calc_hours(year: int, week: int) -> timedelta:
    records = repository.get_by_year_and_week(year, week)
    return reduce(lambda x, y: x + y, map(lambda record: record.duration(), records))


def split_delta(delta):
    days, seconds = delta.days, delta.seconds
    total_minutes = days * 24 * 60 + seconds // 60
    minutes = int(math.fmod(total_minutes, 60))
    hours = int(total_minutes / 60)
    signed_minutes = minutes if delta < timedelta() and hours == 0 else abs(minutes)
    return hours, minutes, signed_minutes


def timedelta_string(delta):
    hours, minutes, signed_minutes = split_delta(delta)
    out = "{} hours".format(hours)

    if minutes != 0:
        out = out + ", {} minutes".format(signed_minutes)

    return out


def timedelta_string_short(delta):
    hours, minutes, signed_minutes = split_delta(delta)
    signed_minutes = minutes if delta < timedelta() and hours == 0 else abs(minutes)
    return "{: 5}h {: 3}m".format(hours, signed_minutes)


def logs(file_name, width):
    file = open(file_name, 'r')
    logs = Table(expand=True, box=box.ROUNDED, width=width, style="gold1")
    logs.add_column("Day")
    logs.add_column("Time")
    logs.add_column("Duration")
    for line in file.readlines():
        columns = line.strip().split(" ")
        if columns[1] == '🤒':
            logs.add_row(columns[0], columns[1], columns[2])
        else:
            logs.add_row(columns[0], ''.join(columns[1:4]), columns[4])
    return logs


def get_record_table(year: int, week: int, width) -> Table:
    records = repository.get_by_year_and_week(year, week)
    table = Table(expand=True, box=box.ROUNDED, width=width, style="gold1")
    table.add_column("Day")
    table.add_column("Time")
    table.add_column("Duration")
    for record in records:
        table.add_row(record.str_day(), record.str_time(), record.str_duration())
    return table


def hours(arg_year, arg_week):
    today = datetime.today()
    year = arg_year if arg_year else today.year
    week = arg_week if arg_week else today.isocalendar().week

    summa = calc_hours(year, week)

    width = 50
    record_table = get_record_table(year, week, width)

    total = "{}".format(timedelta_string(summa))

    required, week_holidays, = weekly_and_holidays(year, week)
    ot = summa - required
    total_req = "{}".format(timedelta_string(required), )
    total_ot = "{}".format(timedelta_string(ot))

    holidays = "Number of holidays: {}".format(week_holidays)

    progress = Progress(
        BarColumn(),
        TaskProgressColumn(style=Style(bold=True)))
    task_id = progress.add_task(description="Percent", total=100)
    progress.update(task_id, advance=round((summa / required) * 100))
    summary = Group(
        record_table,
        Panel(total, title="Total", title_align="left", width=width, style="spring_green1"),
        Panel(total_req, title="Required", title_align="left", width=width, style="deep_sky_blue1"),
        Panel(total_ot, title="Overtime", title_align="left", width=width, style="deep_pink2"),
        Panel(progress, title="Progress", title_align="left", width=width, style="medium_purple1"),
        Panel(holidays, width=width, style="gray62")
    )
    print()
    print(Panel(summary, title=":stopwatch:  Hours for week {} in {}".format(week, year),
                title_align="left", expand=False))
