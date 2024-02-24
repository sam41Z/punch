from datetime import time, date, datetime
from typing import Callable

from rich.console import Console
from simple_term_menu import TerminalMenu

import datetime_parser
import printer
import timerecord

console = Console()


def interactive_mode():
    options = ["[a] add", "[r] remove", "[h] hours", "[o] overtime"]
    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()
    match index:
        case 0:
            tpd_prompt("Creating", lambda day, starts_at, ends_at: timerecord.add(day, starts_at, ends_at))
        case 1:
            delete_prompt()
        case 2:
            raise NotImplementedError
        case 3:
            raise NotImplementedError


def delete_prompt():
    options = ["[t] this week", "[o] other week", "[m] manual"]
    terminal_menu = TerminalMenu(options)
    index = terminal_menu.show()
    match index:
        case 0:
            today = date.today()
            week_delete_prompt(today.year, today.isocalendar().week)
        case 1:
            raise NotImplementedError
        case 2:
            tpd_prompt("Deleting", lambda day, starts_at, ends_at: timerecord.remove(day, starts_at, ends_at))


def week_delete_prompt(year: int, week: int):
    records = timerecord.get_by_year_and_week(year, week)
    options = list(map(lambda r: r.str_record(), records))
    terminal_menu = TerminalMenu(options, multi_select=True, show_multi_select_hint=True, )
    indexes = terminal_menu.show()
    selected = [records[i] for i in indexes]
    printer.print_record_table(selected)
    answer = console_input("Are you sure you want delete these items? (y/n)")
    if answer == "y":
        timerecord.remove_multiple(selected)
    else:
        print("No")


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
        input_str = console_input(prompt)
        try:
            return action(input_str)
        except ValueError as e:
            printer.print_error(str(e))
            prompt = "Try again: "


def console_input(prompt: str) -> str:
    return console.input("[bold red]> [/bold red]{0}: ".format(prompt))
