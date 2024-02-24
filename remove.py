from datetime import datetime

from rich import print
from rich.console import Group
from rich.panel import Panel

from files import get_file_path_by_date
from hours import logs


def remove(arg_offset, arg_num):
    date_time = datetime.today()
    filename = get_file_path_by_date(date_time.date())
    with open(filename, 'r+') as file:
        lines = file.readlines()
        file.seek(0)
        file.truncate()
        r_start = max(arg_offset, arg_num)
        new_lines = lines[:-r_start]
        if arg_offset > arg_num:
            new_lines = new_lines + lines[-(arg_offset - arg_num):]
        file.writelines(new_lines)

    width = 50
    info = Group(
        Panel("Removed {} logs".format(arg_num), width=width, style="deep_pink2"),
        logs(filename, width)
    )
    print()
    print(Panel(info, title=":chart_decreasing:", title_align="left", expand=False))
