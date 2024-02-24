from datetime import time, date, datetime
from typing import Callable

from rich.console import Console
from simple_term_menu import TerminalMenu

import datetime_parser
import hours
import printer
import timerecord

console = Console()


def interactive_mode():
    options = ["[a] add", "[h] hours", "[r] remove"]
    terminal_menu = TerminalMenu(options, title="Do and view")
    index = terminal_menu.show()
    match index:
        case 0:
            tpd_prompt("Add", lambda day, starts_at, ends_at: timerecord.add(day, starts_at, ends_at))
        case 1:
            hours_prompt()
        case 3:
            delete_prompt()


def hours_prompt():
    options = ["[t] this week", "[o] other week"]
    terminal_menu = TerminalMenu(options, title="Hours")
    index = terminal_menu.show()
    match index:
        case 0:
            today = date.today()
            hours.hours(today.year, today.isocalendar().week)
        case 1:
            year, week = week_prompt()
            hours.hours(year, week)


def delete_prompt():
    options = ["[t] this week", "[o] other week", "[m] manual"]
    terminal_menu = TerminalMenu(options, title="Remove")
    index = terminal_menu.show()
    match index:
        case 0:
            today = date.today()
            week_delete_prompt(today.year, today.isocalendar().week)
        case 1:
            year, week = week_prompt()
            week_delete_prompt(year, week)
        case 2:
            tpd_prompt("Remove", lambda day, starts_at, ends_at: timerecord.remove(day, starts_at, ends_at))


def week_prompt():
    year = retryable_input("Enter year", lambda y: datetime_parser.parse_year(y), 3).year
    week = retryable_input("Enter week number", lambda w: datetime_parser.parse_week(w), 3).isocalendar().week
    printer.print_success("Year {0}, week {1}".format(year, week))
    return year, week


def week_delete_prompt(year: int, week: int):
    records = timerecord.get_by_year_and_week(year, week)
    if len(records) == 0:
        printer.print_success("Empty. No records to delete.")
        return
    options = list(map(lambda r: r.str_record(), records))
    terminal_menu = TerminalMenu(options, title="Select the records to remove", multi_select=True,
                                 show_multi_select_hint=True, )
    indexes = terminal_menu.show()
    selected = [records[i] for i in indexes]
    printer.print_record_table(selected)
    answer = console_input("Are you sure you want delete these items? (y/n)")
    if answer == "y":
        timerecord.remove_multiple(selected)
    else:
        printer.print_success("Successfully aborted.")


def tpd_prompt(prompt_prefix: str, action: Callable[[date, time, time], None]):
    options = ["[t] today", "[w] this week", "[d] any date"]
    terminal_menu = TerminalMenu(options, title=prompt_prefix)
    menu_entry_index = terminal_menu.show()

    if menu_entry_index == 0:
        day = date.today()
        time_span_input(lambda starts_at, ends_at: action(day, starts_at, ends_at))
    elif menu_entry_index == 1:
        weekday_prompt(prompt_prefix, action)
    elif menu_entry_index == 2:
        date_prompt(prompt_prefix, action)


def weekday_prompt[T](prompt_prefix: str, action: Callable[[date, time, time], None]):
    weekdays = list(map(lambda d: date.fromisocalendar(2024, 1, d).strftime("%A"), range(1, 8)))
    terminal_menu = TerminalMenu(weekdays, title="Choose a day")
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
