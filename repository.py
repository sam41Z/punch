from typing import Sequence
from datetime import datetime, date, time
from sqlalchemy import select, or_, and_, func, ColumnElement
from database import Session, TimeRecordDb
from model import TimeRecord


def create_record(new: TimeRecord) -> None:
    new_db_record = TimeRecordDb(started_at=new.started_at, ended_at=new.ended_at)
    with Session.begin() as session:
        count: int = session.execute(select(func.count()).select_from(TimeRecordDb).where(
            range_overlaps(new.started_at, new.ended_at))).scalar()
        print(count)
        if count > 0:
            raise ValueError("Time record overlaps with existing")
        session.add(new_db_record)


def range_overlaps(started_at: datetime, ended_at: datetime) -> ColumnElement[bool]:
    return or_(and_(TimeRecordDb.started_at < ended_at, TimeRecordDb.ended_at <= ended_at),
               and_(TimeRecordDb.started_at <= started_at, TimeRecordDb.ended_at > started_at),
               and_(TimeRecordDb.started_at >= started_at, TimeRecordDb.ended_at <= ended_at),
               and_(TimeRecordDb.started_at <= started_at, TimeRecordDb.ended_at >= ended_at))


def get_range(started_at: datetime, ended_at: datetime) -> Sequence[TimeRecord]:
    with Session.begin() as session:
        query = select(TimeRecordDb).where(range_overlaps(started_at, ended_at))
        scalars = session.scalars(query).all()
        return list(map(lambda x: TimeRecord(x.started_at, x.ended_at), scalars))


def get_by_year_and_week(year: int, week: int) -> Sequence[TimeRecord]:
    range_start = datetime.combine(date.fromisocalendar(year, week, 1), time(0))
    range_end = datetime.combine(date.fromisocalendar(year, week, 7), time(23, 59))
    print(str(range_start) + " " + str(range_end))
    return get_range(range_start, range_end)
