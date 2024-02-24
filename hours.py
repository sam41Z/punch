import math
from datetime import datetime, timedelta
from functools import reduce

from rich import print
from rich.console import Group
from rich.panel import Panel
from rich.progress import Progress, BarColumn, TaskProgressColumn
from rich.style import Style

from holidays import weekly_and_holidays
import repository
from printer import get_record_table


def calc_hours(year: int, week: int) -> timedelta:
    print(str(year) + " " + str(week))
    records = repository.get_by_year_and_week(year, week)
    return reduce(lambda x, y: x + y, map(lambda record: record.duration(), records), timedelta())


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


def hours(arg_year, arg_week):
    today = datetime.today()
    year = arg_year if arg_year else today.year
    week = arg_week if arg_week else today.isocalendar().week

    summa = calc_hours(year, week)

    width = 50
    records = repository.get_by_year_and_week(year, week)
    record_table = get_record_table(records, width)

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
