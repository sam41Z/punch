from datetime import timedelta


def num_holidays(year, week):
    return HOLIDAYS[int(year)].get(int(week), 0.0)


def weekly_and_holidays(year, week):
    holidays = num_holidays(year, week)
    return timedelta(hours=(32 / 5 * (5 - holidays))), holidays


HOLIDAYS = {
    2023: {1: 1, 14: 1, 15: 1, 16: 0.5, 18: 1, 20: 1, 22: 1, 31: 1, 37: 0.5, 52: 2},
    2024: {1: 2, 13: 1, 14: 1, 16: 0.5, 18: 1, 19: 1, 21: 1, 31: 1, 37: 0.5, 52: 2.5}
}
