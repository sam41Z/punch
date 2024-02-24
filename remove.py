from datetime import datetime
from files import get_file_path_by_date
from rich import print
from rich.console import Group
from rich.panel import Panel
from hours import logs


def remove(arg_num):
    date_time = datetime.today()
    filename = get_file_path_by_date(date_time.date())
    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        file.writelines(lines[:-arg_num])

    width = 50
    info = Group(
        Panel("Removed {} lines".format(arg_num),  width=width, style="deep_pink2"),
        logs(filename, width)
    )
    print(Panel(info, title=":chart_decreasing:", title_align="left", expand=False))
