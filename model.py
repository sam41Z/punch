from datetime import datetime, timedelta, date, time


class TimeRecord:
    def __init__(self, starts_at: datetime, ends_at: datetime):
        if ends_at < starts_at:
            msg = "End time ({}) is before start time ({})".format(ends_at.strftime("%H:%M"),
                                                                   starts_at.strftime("%H:%M"))
            raise ValueError(msg)
        if starts_at.tzinfo is None or ends_at.tzinfo is None:
            raise ValueError("No timezone info!")

        self.starts_at = starts_at
        self.ends_at = ends_at

    @classmethod
    def create(cls, day: date, starts_at: time, ends_at: time):
        return cls(datetime.combine(day, starts_at).astimezone(), datetime.combine(day, ends_at).astimezone())

    def duration(self) -> timedelta:
        return self.ends_at - self.starts_at

    def str_day(self) -> str:
        return self.starts_at.strftime("%a")

    def str_time(self) -> str:
        return self.starts_at.strftime("%H:%M") + "-" + self.ends_at.strftime("%H:%M")

    def str_duration(self):
        # return str(self.ends_at - self.starts_at)[:-3]
        return ':'.join(str(self.ends_at - self.starts_at).split(':')[:2])
