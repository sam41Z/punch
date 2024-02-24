from datetime import datetime


def parse_time(s):
    try:
        return datetime.strptime(s, "%H:%M").time()
    except ValueError:
        pass
    try:
        return datetime.strptime(s, "%H").time()
    except ValueError:
        msg = "Not a valid time: {0!r}".format(s)
        raise ValueError(msg)


def parse_time_span(s):
    try:
        times = s.split('-')
        if len(times) != 2:
            raise ValueError
        start = times[0]
        end = times[1]
        return parse_time(start), parse_time(end)
    except ValueError:
        msg = "Not a valid time span: {0!r}".format(s)
        raise ValueError(msg)


def parse_date(s):
    try:
        return datetime.strptime(s, "%Y-%m-%d")
    except ValueError:
        msg = "Not a valid date: {0!r}".format(s)
        raise ValueError(msg)


def parse_year(s):
    try:
        return datetime.strptime(s, "%Y")
    except ValueError:
        msg = "Not a valid year: {0!r}".format(s)
        raise ValueError(msg)


def parse_week(week_str: str, year: int):
    try:
        return datetime.strptime("{0},{1},1".format(week_str, year), "%W,%Y,%w")
    except ValueError:
        msg = "Not a valid week number: {0!r}".format(s)
        raise ValueError(msg)
