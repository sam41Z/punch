from datetime import time, date, datetime
from typing import Callable

from rich.console import Console
from simple_term_menu import TerminalMenu

import add
import datetime_parser
import printer

console = Console()


def interactive_mode():
    options = ["[a] add", "[r] remove", "[h] hours", "[o] overtime"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()
    if menu_entry_index == 0:
        tpd_prompt("Creating", lambda day, starts_at, ends_at: add.add(day, starts_at, ends_at))


def tpd_prompt(prompt_prefix: str, action: Callable[[date, time, time], None]):
    options = ["[t] today", "[p] prefix", "[d] date"]
    terminal_menu = TerminalMenu(options)
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == 0:
        day = date.today()
        time_span_input(lambda starts_at, ends_at: action(day, starts_at, ends_at))
    elif menu_entry_index == 1:
        prefix_prompt(prompt_prefix, action)
    elif menu_entry_index == 2:
        date_prompt(prompt_prefix, action)


def prefix_prompt[T](prompt_prefix: str, action: Callable[[date, time, time], None]):
    weekdays = list(map(lambda d: date.fromisocalendar(2024, 1, d).strftime("%A"), range(1, 8)))
    terminal_menu = TerminalMenu(weekdays)
    index = terminal_menu.show()
    today = date.today()
    day = datetime.strptime(weekdays[index] + "," + today.strftime("%W,%Y"), "%A,%W,%Y")
    printer.print_success(day.strftime(prompt_prefix + " entry for %A, %d %B %Y"))

    time_span_input(lambda starts_at, ends_at: action(day, starts_at, ends_at))


def date_prompt[T](prompt_prefix: str, action: Callable[[date, time, time], None]):
    day = retryable_input("Enter date (like YYYY-MM-DD)",
                          lambda date_str: datetime_parser.parse_date(date_str), 3)
    printer.print_success(day.strftime(prompt_prefix + " entry for %A, %d %B %Y"))

    time_span_input(lambda starts_at, ends_at: action(day, starts_at, ends_at))


def time_span_input[T](action: Callable[[time, time], T]) -> [T]:
    def after_time_input(time_span: str) -> None:
        starts_at, ends_at = datetime_parser.parse_time_span(time_span)
        action(starts_at, ends_at)

    retryable_input("Enter time span (like HH-HH or HH:mm-HH:mm)", after_time_input, 3)


def retryable_input[T](question: str, action: Callable[[str], T], retries: int) -> T:
    prompt = question
    for i in range(0, retries):
        input_str = console.input("[bold red]> [/bold red]{0}: ".format(prompt))
        try:
            return action(input_str)
        except ValueError as e:
            printer.print_error(str(e))
            prompt = "Try again: "
