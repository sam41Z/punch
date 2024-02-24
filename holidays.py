import os
from datetime import timedelta
from files import get_base_path


def num_holidays(year, week):
    file_name = get_file_name(year)
    file = open(file_name, 'r')
    for line in file:
        week_str, num_str = line.split(' ', 1)

        if int(week_str) == week:
            return float(num_str)
    return 0.0


def weekly_and_holidays(year, week):
    holidays = num_holidays(year, week)
    return timedelta(hours=(32 / 5 * (5 - holidays))), holidays


def get_file_name(year):
    return "{0}/{1}/holidays".format(get_base_path(), year)
