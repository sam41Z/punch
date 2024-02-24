from datetime import datetime, timedelta
from files import get_file_path_by_yw, parse_path
from holidays import num_holidays, weekly_and_holidays
from hours import calc_hours, timedelta_string


def overtime(arg_week):
    date = datetime.today()
    current_year = date.strftime("%Y")
    current_week = int(date.strftime("%U"))

    if arg_week:
        weeks = range(arg_week, current_week)
        files = set()
        for week in weeks:
            files.add(get_file_path_by_yw(current_year, week))
    else:
        files = parse_path([current_year])

    summa = timedelta()
    for week in weeks:
        file = get_file_path_by_yw(current_year, week)
        required, holidays = weekly_and_holidays(current_year, week)
        debt = calc_hours(file) - required
        summa = summa + debt

    out = "Total overtime: {}".format(timedelta_string(summa))
    info = "Week {} to {}".format(min(weeks), max(weeks))

    sep = ""
    for i in range(len(out)):
        sep = sep + "#"
    print(sep)
    print()
    print(out)
    print()
    print(info)
    print()
    print(sep)
