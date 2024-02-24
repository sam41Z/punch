from datetime import datetime, date

import repository
from printer import print_with_new

from repository import create_record
from model import TimeRecord


def add(arg_date, arg_time, arg_prefix):
    day = arg_date if arg_date else date.today()
    if arg_prefix:
        day = datetime.strptime(arg_prefix + "," + day.strftime("%W,%Y"), "%a,%W,%Y")

    start_time, end_time = arg_time
    start = datetime.combine(day, start_time)
    end = datetime.combine(day, end_time)

    new_record = TimeRecord(start, end)
    create_record(new_record)
    print_info(new_record)


def print_info(new_record: TimeRecord):
    year = new_record.started_at.year
    week = new_record.started_at.isocalendar().week
    records = repository.get_by_year_and_week(year, week)

    print_with_new(new_record, records)
