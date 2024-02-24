from typing import Sequence

from rich import box
from rich.table import Table

from model import TimeRecord


def get_record_table(records: Sequence[TimeRecord], width: int) -> Table:
    table = Table(expand=True, box=box.ROUNDED, width=width, style="gold1")
    table.add_column("Day")
    table.add_column("Time")
    table.add_column("Duration")
    for record in records:
        table.add_row(record.str_day(), record.str_time(), record.str_duration())
    return table
