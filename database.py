from datetime import datetime
from sqlalchemy import create_engine
from sqlalchemy import TIMESTAMP
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker
from files import get_base_path

url = "sqlite:///" + get_base_path() + "/db.db"
print(url)
engine = create_engine(url, echo=True)
Session = sessionmaker(engine)


class Base(DeclarativeBase):
    type_annotation_map = {
        datetime: TIMESTAMP(timezone=True),
    }


class TimeRecordDb(Base):
    __tablename__ = "time_record"

    id: Mapped[int] = mapped_column(primary_key=True)
    started_at: Mapped[datetime]
    ended_at: Mapped[datetime]


def setup():
    Base.metadata.create_all(engine)