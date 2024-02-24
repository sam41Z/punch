from typing import Sequence
from datetime import datetime, date, time
from sqlalchemy import select, or_, and_, func
from database import Session, TimeRecordDb
from model import TimeRecord


def create_record(new: TimeRecord) -> None:
    new_db_record = TimeRecordDb(started_at=new.started_at, ended_at=new.ended_at)
    with Session.begin() as session:
        count: int = session.execute(select(func.count()).select_from(TimeRecordDb).where(
            or_(and_(TimeRecordDb.started_at < new.ended_at, TimeRecordDb.ended_at <= new.ended_at),
                and_(TimeRecordDb.started_at <= new.started_at, TimeRecordDb.ended_at > new.started_at),
                and_(TimeRecordDb.started_at >= new.started_at, TimeRecordDb.ended_at <= new.ended_at),
                and_(TimeRecordDb.started_at <= new.started_at, TimeRecordDb.ended_at >= new.ended_at)))).scalar()
        print(count)
        if count > 0:
            raise ValueError("Time record overlaps with existing")
        session.add(new_db_record)


def get_range(start: datetime, end: datetime) -> Sequence[TimeRecord]:
    with Session.begin() as session:
        query = select(TimeRecordDb).where(or_(TimeRecordDb.ended_at > start, TimeRecordDb.started_at < end)).order_by(
            TimeRecordDb.started_at)
        scalars = session.scalars(query).all()
        return list(map(lambda x: TimeRecord(x.started_at, x.ended_at), scalars))


def get_by_year_and_week(year: int, week: int) -> Sequence[TimeRecord]:
    range_start = datetime.combine(date.fromisocalendar(year, week, 1), time(0))
    range_end = datetime.combine(date.fromisocalendar(year, week, 7), time(23, 59))
    return get_range(range_start, range_end)
