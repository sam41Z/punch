from datetime import timedelta
from functools import reduce

from holidays import weekly_and_holidays
from printer import print_weekly, print_overtime
from repository import Repository


def calc_hours(year: int, week: int) -> timedelta:
    records = Repository().get_by_year_and_week(year, week)
    return reduce(lambda x, y: x + y, map(lambda record: record.duration(), records), timedelta())


def hours_of_week(year: int, week: int):
    worked = calc_hours(year, week)
    records = Repository().get_by_year_and_week(year, week)
    required, week_holidays, = weekly_and_holidays(year, week)

    print_weekly(records, required, worked, week_holidays, year, week)


def accumulated_hours(year: int, from_week: int, to_week: int):
    weeks = range(from_week, to_week + 1)
    weekly_overtime = []
    for week in weeks:
        worked = calc_hours(year, week)
        required, week_holidays, = weekly_and_holidays(year, week)
        weekly_overtime.append((week, worked - required))

    print_overtime(weekly_overtime, year)
