from datetime import datetime


class TimeRecord:
    def __init__(self, started_at: datetime, ended_at: datetime):
        if ended_at < started_at:
            msg = "End time ({}) is before start time ({})".format(ended_at.strftime("%H:%M"), started_at.strftime("%H:%M"))
            raise ValueError(msg)
        self.started_at = started_at
        self.ended_at = ended_at

    def str_day(self) -> str:
        return self.started_at.strftime("%a")

    def str_time(self) -> str:
        return self.started_at.strftime("%H:%M") + "-" + self.ended_at.strftime("%H:%M")

    def str_duration(self):
        # return str(self.ended_at - self.started_at)[:-3]
        return ':'.join(str(self.ended_at - self.started_at).split(':')[:2])
