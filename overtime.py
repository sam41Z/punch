from datetime import datetime, timedelta
from files import get_file_path_by_yw, parse_path
from holidays import num_holidays, weekly_and_holidays
from hours import calc_hours, timedelta_string, timedelta_string_short
from rich.table import Table
from rich import print, box
from rich.console import Group
from rich.panel import Panel
from rich.text import Text


def overtime(arg_week):
    width = 50

    date = datetime.today()
    year = date.strftime("%Y")
    current_week = int(date.strftime("%U"))

    weeks = range(arg_week, current_week + 1)
    total = timedelta()

    weekly_ot = Table(expand=True, box=box.ROUNDED, width=width, style="gold1")
    weekly_ot.add_column("Week")
    weekly_ot.add_column("Overtime")
    for week in weeks:
        file_name = get_file_path_by_yw(year, week)
        summa = calc_hours(filename=file_name)
        required, week_holidays, = weekly_and_holidays(year, week)
        ot = summa - required
        total = total + ot

        prefix = " "
        if ot < timedelta():
            style = "deep_pink2"
            prefix = ""
        elif ot > timedelta():
            style = "spring_green1"
        else:
            style = ""

        weekly_ot.add_row("{}".format(week), Text(timedelta_string_short(ot), style=style))

    summary = Group(
        weekly_ot,
        Panel(timedelta_string(total), title="Total Overtime", title_align="left", width=width, style="deep_sky_blue1"),
    )
    print()
    print(Panel(summary, title=":stopwatch:  Overtime from week {} to {} in {}".format(arg_week, current_week, year),
                title_align="left", expand=False))
