from datetime import timedelta
from functools import reduce
from typing import Sequence

import math
from rich import box, print
from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TaskProgressColumn
from rich.style import Style
from rich.table import Table
from rich.text import Text

from model import TimeRecord

width = 50


def get_record_table(records: Sequence[TimeRecord]) -> Table:
    table = Table(expand=True, box=box.ROUNDED, width=width, style="gold1")
    table.add_column("Day")
    table.add_column("Time")
    table.add_column("Duration")
    for record in records:
        table.add_row(record.str_day(), record.str_time(), record.str_duration())
    return table


def print_record_table(records: Sequence[TimeRecord]):
    print(get_record_table(records))


def print_weekly(records: Sequence[TimeRecord], required: timedelta, worked: timedelta, week_holidays, year, week):
    record_table = get_record_table(records)
    holidays = "Number of holidays: {}".format(week_holidays)
    progress = Progress(BarColumn(), TaskProgressColumn(style=Style(bold=True)))
    task_id = progress.add_task(description="Percent", total=100)
    progress.update(task_id, advance=round((worked / required) * 100))
    summary = Group(record_table,
                    Panel(timedelta_string(worked), title="Total", title_align="left", width=width,
                          style="spring_green1"),
                    Panel(timedelta_string(required), title="Required", title_align="left", width=width,
                          style="deep_sky_blue1"),
                    Panel(timedelta_string(worked - required), title="Overtime", title_align="left", width=width,
                          style="deep_pink2"),
                    Panel(progress, title="Progress", title_align="left", width=width, style="medium_purple1"),
                    Panel(holidays, width=width, style="gray62")
                    )
    print()
    print(Panel(summary, title=":stopwatch:  Hours for week {} in {}".format(week, year),
                title_align="left", expand=False))


def print_overtime(weekly_overtime, year):
    weekly_ot = Table(expand=True, box=box.ROUNDED, width=width, style="gold1")
    weekly_ot.add_column("Week")
    weekly_ot.add_column("Overtime")
    for (week, overtime) in weekly_overtime:
        if overtime < timedelta():
            style = "deep_pink2"
        elif overtime > timedelta():
            style = "spring_green1"
        else:
            style = ""

        weekly_ot.add_row("{}".format(week), Text(timedelta_string_short(overtime), style=style))

    first_week = min(map(lambda o: o[0], weekly_overtime))
    last_week = max(map(lambda o: o[0], weekly_overtime))
    total = reduce(lambda x, y: x + y, map(lambda o: o[1], weekly_overtime), timedelta())
    summary = Group(
        weekly_ot,
        Panel(timedelta_string(total), title="Total Overtime", title_align="left", width=width, style="deep_sky_blue1"),
    )
    print()
    print(Panel(summary, title=":stopwatch:  Overtime from week {} to {} in {}".format(first_week, last_week, year),
                title_align="left", expand=False))


def print_with_selected(selected: Sequence[TimeRecord], records: Sequence[TimeRecord], title: str):
    entries = "\n".join(map(lambda r: r.str_record(), selected))
    print( Panel(entries, title=title, width=width, title_align="left", style="spring_green1"))
    print(get_record_table(records))


def print_success(content: str):
    print(Panel(content, width=width, title_align="left", style="spring_green1"))


def print_error(content: str):
    print(Panel(content, width=width, title_align="left", style="deep_pink2"))


def timedelta_string(delta) -> str:
    hours, minutes, signed_minutes = split_delta(delta)
    out = "{} hours".format(hours)

    if minutes != 0:
        out = out + ", {} minutes".format(signed_minutes)

    return out


def timedelta_string_short(delta):
    hours, minutes, signed_minutes = split_delta(delta)
    signed_minutes = minutes if delta < timedelta() and hours == 0 else abs(minutes)
    return "{: 5}h {: 3}m".format(hours, signed_minutes)


def split_delta(delta):
    days, seconds = delta.days, delta.seconds
    total_minutes = days * 24 * 60 + seconds // 60
    minutes = int(math.fmod(total_minutes, 60))
    hours = int(total_minutes / 60)
    signed_minutes = minutes if delta < timedelta() and hours == 0 else abs(minutes)
    return hours, minutes, signed_minutes
