from typing import Sequence
from datetime import datetime, date, time
from sqlalchemy import select, or_, and_, func, ColumnElement
from database import Database, TimeRecordRow
from model import TimeRecord


class Repository:

    def __init__(self, database=Database()):
        self.Session = database.Session

    @classmethod
    def test(cls):
        return cls(database=Database.test())

    def create_record(self, new: TimeRecord) -> None:
        new_db_record = TimeRecordRow(starts_at=new.starts_at, ends_at=new.ends_at)
        with self.Session.begin() as session:
            count: int = session.execute(select(func.count()).select_from(TimeRecordRow).where(
                self.range_overlaps(new.starts_at, new.ends_at))).scalar()
            if count > 0:
                raise ValueError("Time record overlaps with existing")
            session.add(new_db_record)

    @staticmethod
    def range_overlaps(starts_at: datetime, ends_at: datetime) -> ColumnElement[bool]:
        return or_(
            and_(TimeRecordRow.starts_at < ends_at, TimeRecordRow.ends_at >= ends_at),
            and_(TimeRecordRow.starts_at <= starts_at, TimeRecordRow.ends_at > starts_at),
            and_(TimeRecordRow.starts_at >= starts_at, TimeRecordRow.ends_at <= ends_at),
            and_(TimeRecordRow.starts_at <= starts_at, TimeRecordRow.ends_at >= ends_at)
        )

    def get_range(self, starts_at: datetime, ends_at: datetime) -> Sequence[TimeRecord]:
        with self.Session.begin() as session:
            query = select(TimeRecordRow).where(self.range_overlaps(starts_at, ends_at)).order_by(
                TimeRecordRow.starts_at)
            scalars = session.scalars(query).all()
            return list(map(lambda x: TimeRecord(x.starts_at, x.ends_at), scalars))

    def get_by_year_and_week(self, year: int, week: int) -> Sequence[TimeRecord]:
        range_start = datetime.combine(date.fromisocalendar(year, week, 1), time(0))
        range_end = datetime.combine(date.fromisocalendar(year, week, 7), time(23, 59))
        return self.get_range(range_start, range_end)
