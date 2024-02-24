from datetime import datetime, timedelta
from functools import reduce

from holidays import weekly_and_holidays
import repository
from printer import print_weekly


def calc_hours(year: int, week: int) -> timedelta:
    records = repository.get_by_year_and_week(year, week)
    return reduce(lambda x, y: x + y, map(lambda record: record.duration(), records), timedelta())


def hours(arg_year, arg_week):
    today = datetime.today()
    year = arg_year if arg_year else today.year
    week = arg_week if arg_week else today.isocalendar().week

    worked = calc_hours(year, week)
    records = repository.get_by_year_and_week(year, week)
    required, week_holidays, = weekly_and_holidays(year, week)

    print_weekly(records, required, worked, week_holidays, year, week)
