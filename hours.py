from datetime import datetime, timedelta
from functools import reduce

from holidays import weekly_and_holidays
from printer import print_weekly
from repository import Repository


def calc_hours(year: int, week: int) -> timedelta:
    records = Repository().get_by_year_and_week(year, week)
    return reduce(lambda x, y: x + y, map(lambda record: record.duration(), records), timedelta())


def hours(year, week):
    worked = calc_hours(year, week)
    records = Repository().get_by_year_and_week(year, week)
    required, week_holidays, = weekly_and_holidays(year, week)

    print_weekly(records, required, worked, week_holidays, year, week)
