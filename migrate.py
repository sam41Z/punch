import os
from datetime import date, datetime, time
from os.path import expanduser

from model import TimeRecord


def get_file_path_by_yw(year, week):
    return "{0}/{1}/w{2:02d}.hr".format(get_base_path(), year, week)


def get_base_path():
    return expanduser("~/.config/punch")


def weeks_for_year(year):
    last_week = date(year, 12, 28)
    return range(1, last_week.isocalendar().week)


def parse_time(time_str: str) -> time:
    return datetime.strptime(time_str, "%H:%M").time()


def parse_date(year: int, week: int, weekday: str) -> date:
    date_str = "{0},{1},{2}".format(weekday, week, year)
    return datetime.strptime(date_str, "%a,%W,%Y").date()


class Migration:

    def __init__(self, repository):
        self.repository = repository

    def migrate(self, year: int):
        for week in weeks_for_year(year):
            filename = get_file_path_by_yw(year, week)
            if not os.path.exists(filename):
                print("File not found, skipping. File: {0}".format(filename))
                continue
            with open(filename) as file:
                for line in file:
                    chunks = line.split(' ')
                    day = parse_date(year, week, chunks[0])
                    starts_at = parse_time(chunks[1])
                    ends_at = parse_time(chunks[3])
                    record = TimeRecord.create(day, starts_at, ends_at)
                    self.repository.create_record(record)
                    print("Migrated: " + record.str_record())
