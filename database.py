from datetime import datetime
from os.path import expanduser

from sqlalchemy import create_engine, TypeDecorator, Integer
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Database:
    url = "sqlite:///" + expanduser("~/.config/punch") + "/db.db"

    def __init__(self, url=url):
        engine = create_engine(url)
        self.Session = sessionmaker(engine)
        Base.metadata.create_all(engine)

    @classmethod
    def test(cls):
        return cls(url="sqlite://")


# define a custom type for unix timestamp
class UnixTimestamp(TypeDecorator):
    # convert unix timestamp to datetime object
    impl = Integer
    cache_ok = True

    # convert datetime object to unix timestamp when inserting data to database
    def process_bind_param(self, value: datetime, dialect):
        return int(value.timestamp())

    # convert unix timestamp to  datetime object retrieving data from database
    def process_result_value(self, value, dialect):
        return datetime.fromtimestamp(value).astimezone()


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: UnixTimestamp,
    }


class TimeRecordRow(Base):
    __tablename__ = "time_record"

    id: Mapped[int] = mapped_column(primary_key=True)
    starts_at: Mapped[datetime]
    ends_at: Mapped[datetime]
