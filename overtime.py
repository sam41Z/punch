from datetime import datetime, timedelta

from rich import print, box
from rich.console import Group
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

from holidays import weekly_and_holidays
from hours import calc_hours, timedelta_string, timedelta_string_short


def overtime(arg_week):
    width = 50

    today = datetime.today()
    year = today.year
    current_week = today.isocalendar().week

    weeks = range(arg_week, current_week + 1)
    total = timedelta()

    weekly_ot = Table(expand=True, box=box.ROUNDED, width=width, style="gold1")
    weekly_ot.add_column("Week")
    weekly_ot.add_column("Overtime")
    for week in weeks:
        summa = calc_hours(year, week)
        required, week_holidays, = weekly_and_holidays(year, week)
        ot = summa - required
        total = total + ot

        if ot < timedelta():
            style = "deep_pink2"
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
