from typing import Sequence
from datetime import datetime
from sqlalchemy import select, or_
from database import Session, TimeRecordDb


class TimeRecord:
    def __init__(self, started_at: datetime, ended_at: datetime):
        self.started_at = started_at
        self.ended_at = ended_at


def create_record(new: TimeRecord) -> None:
    new_db_record = TimeRecordDb(started_at=new.started_at, ended_at=new.ended_at)
    with Session.begin() as session:
        session.add(new_db_record)


def fetch_range(start: datetime, end: datetime) -> Sequence[TimeRecord]:
    with Session.begin() as session:
        query = select(TimeRecordDb).where(or_(TimeRecordDb.ended_at > start, TimeRecordDb.started_at < end)).order_by(
            TimeRecordDb.started_at)
        scalars = session.scalars(query).all()
        return list(map(lambda x: TimeRecord(x.started_at, x.ended_at), scalars))
