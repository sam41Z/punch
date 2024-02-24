from datetime import datetime, date, time
from typing import Sequence

from sqlalchemy import select, or_, and_, func, ColumnElement
from sqlalchemy.exc import NoResultFound, MultipleResultsFound

from database import Database, TimeRecordRow
from model import TimeRecord


class Repository:

    def __init__(self, database=Database()):
        self.Session = database.Session

    @classmethod
    def test(cls):
        return cls(database=Database.test())

    def create_record(self, new: TimeRecord):
        with self.Session.begin() as session:
            count: int = session.execute(select(func.count()).select_from(TimeRecordRow).where(
                self.range_overlaps(new.starts_at, new.ends_at))).scalar()
            if count > 0:
                raise ValueError("Time record overlaps with existing")
            new_db_record = TimeRecordRow(starts_at=new.starts_at, ends_at=new.ends_at)
            session.add(new_db_record)

    def remove_record(self, record: TimeRecord):
        with self.Session.begin() as session:
            query = select(TimeRecordRow).where(
                and_(TimeRecordRow.starts_at == record.starts_at, TimeRecordRow.ends_at == record.ends_at)).order_by(
                TimeRecordRow.starts_at)
            try:
                result = session.scalars(query).one()
            except (NoResultFound, MultipleResultsFound):
                raise ValueError("None or multiple records found with the same range")

            session.delete(result)

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
