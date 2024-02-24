from datetime import date, time
from typing import Sequence

from model import TimeRecord
from printer import print_with_new
from repository import Repository


def add(day: date, starts_at: time, ends_at: time):
    new_record = TimeRecord.create(day, starts_at, ends_at)
    Repository().create_record(new_record)
    print_info([new_record], "Added")


def remove(day: date, starts_at: time, ends_at: time):
    record = TimeRecord.create(day, starts_at, ends_at)
    Repository().remove_record(record)
    print_info([record], "Removed")


def remove_multiple(records: Sequence[TimeRecord]):
    for record in records:
        Repository().remove_record(record)

    print_info(records, "Removed")


def get_by_year_and_week(year: int, week: int) -> Sequence[TimeRecord]:
    return Repository().get_by_year_and_week(year, week)


def print_info(selected: Sequence[TimeRecord], title: str):
    year = selected[0].starts_at.year
    week = selected[0].starts_at.isocalendar().week
    records = Repository().get_by_year_and_week(year, week)

    print_with_new(selected, records, title)
