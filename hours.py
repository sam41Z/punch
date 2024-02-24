import math
from datetime import datetime, timedelta
from rich import print, box
from rich.panel import Panel
from rich.style import Style
from rich.table import Table
from rich.console import Group
from rich.progress import Progress, TextColumn, BarColumn, TaskProgressColumn
from rich.text import Text
from files import get_file_path_by_yw
from holidays import num_holidays, weekly_and_holidays
from time import sleep


def calc_hours(filename):
    count = timedelta()
    try:
        with open(filename) as file:
            for line in file:
                chunks = line.split(' ')
                s = chunks[len(chunks) - 1]
                time = datetime.strptime(s, "%H:%M\n").time()
                delta = timedelta(hours=time.hour, minutes=time.minute)
                count += delta
            file.close()
    finally:
        return count


def timedelta_string(delta):
    days, seconds = delta.days, delta.seconds

    total_minutes = days * 24 * 60 + seconds // 60
    minutes = int(math.fmod(total_minutes, 60))
    hours = int(total_minutes / 60)

    signed_minutes = minutes if delta < timedelta() and hours == 0 else abs(minutes)
    out = "{} hours".format(hours)

    if minutes != 0:
        out = out + ", {} minutes".format(signed_minutes)

    return out


def timedelta_string_short(delta):
    days, seconds = delta.days, delta.seconds
    total_minutes = days * 24 * 60 + seconds // 60
    minutes = int(math.fmod(total_minutes, 60))
    hours = int(total_minutes / 60)

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


def hours(arg_year, arg_week):
    date = datetime.today()
    if arg_year:
        year = arg_year
    else:
        year = date.strftime("%Y")

    if arg_week:
        week = arg_week
    else:
        week = int(date.strftime("%U"))

    file_name = get_file_path_by_yw(year, week)
    summa = calc_hours(filename=file_name)

    try:
        width = 50
        logs_table = logs(file_name, width)

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
            logs_table,
            Panel(total, title="Total", title_align="left", width=width, style="spring_green1"),
            Panel(total_req, title="Required", title_align="left", width=width, style="deep_sky_blue1"),
            Panel(total_ot, title="Overtime", title_align="left", width=width, style="deep_pink2"),
            Panel(progress, title="Progress", title_align="left", width=width, style="medium_purple1"),
            Panel(holidays, width=width, style="gray62")
        )
        print()
        print(Panel(summary, title=":stopwatch:  Hours for week {} in {}".format(week, year),
                    title_align="left", expand=False))

    except FileNotFoundError as e:
        print("No logs for week {} in {}".format(week, year))
