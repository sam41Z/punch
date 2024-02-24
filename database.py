from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from os.path import expanduser


class Database:
    url = "sqlite:///" + expanduser("~/.config/punch") + "/db.db"

    def __init__(self, url=url):
        engine = create_engine(url)
        self.Session = sessionmaker(engine)
        Base.metadata.create_all(engine)

    @classmethod
    def test(cls):
        return cls(url="sqlite://")


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }


class TimeRecordRow(Base):
    __tablename__ = "time_record"

    id: Mapped[int] = mapped_column(primary_key=True)
    starts_at: Mapped[datetime]
    ends_at: Mapped[datetime]
