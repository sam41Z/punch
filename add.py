from datetime import datetime, date

from model import TimeRecord
from printer import print_with_new
from repository import Repository


def add(arg_date, arg_time, arg_prefix):
    day = arg_date if arg_date else date.today()
    if arg_prefix:
        day = datetime.strptime(arg_prefix + "," + day.strftime("%W,%Y"), "%a,%W,%Y")

    starts_at, ends_at = arg_time

    new_record = TimeRecord.create(day, starts_at, ends_at)
    Repository().create_record(new_record)
    print_info(new_record)


def print_info(new_record: TimeRecord):
    year = new_record.starts_at.year
    week = new_record.starts_at.isocalendar().week
    records = Repository().get_by_year_and_week(year, week)

    print_with_new(new_record, records)
