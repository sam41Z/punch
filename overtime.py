from datetime import datetime

from holidays import weekly_and_holidays
from hours import calc_hours
from printer import print_overtime


def overtime(arg_week):
    today = datetime.today()
    year = today.year
    current_week = today.isocalendar().week

    weeks = range(arg_week, current_week + 1)
    weekly_overtime = []
    for week in weeks:
        worked = calc_hours(year, week)
        required, week_holidays, = weekly_and_holidays(year, week)
        overtime = worked - required
        weekly_overtime.append((week, overtime))

    print_overtime(weekly_overtime, year)
