from datetime import time, date, datetime
from typing import Callable

from simple_term_menu import TerminalMenu

import datetime_parser
import hours
import printer
import timerecord


def interactive_mode(cursor_index=0):
    options = ["[a] add", "[h] hours", "[r] remove", None, "[e] exit"]
    terminal_menu = TerminalMenu(options, title="Do and view", cursor_index=cursor_index)
    index = terminal_menu.show()
    match index:
        case 0:
            tpd_prompt("Add", lambda day, starts_at, ends_at: timerecord.add(day, starts_at, ends_at),
                       lambda: interactive_mode(cursor_index=0))
        case 1:
            hours_prompt(lambda: interactive_mode(cursor_index=1))
        case 2:
            delete_prompt(lambda: interactive_mode(cursor_index=2))
        case 4:
            exit()


def hours_prompt(back: Callable):
    options = ["[t] this week", "[o] other week", None, "[b] back"]
    terminal_menu = TerminalMenu(options, title="Hours")
    index = terminal_menu.show()
    match index:
        case 0:
            today = date.today()
            hours.hours(today.year, today.isocalendar().week)
        case 1:
            year, week = week_prompt()
            hours.hours(year, week)
        case 3:
            back()


def delete_prompt(back: Callable, cursor_index=0):
    options = ["[t] this week", "[o] other week", None, "[b] back"]
    terminal_menu = TerminalMenu(options, title="Remove", cursor_index=cursor_index)
    index = terminal_menu.show()
    match index:
        case 0:
            today = date.today()
            week_delete_prompt(today.year, today.isocalendar().week)
        case 1:
            year, week = week_prompt()
            week_delete_prompt(year, week)
        case 3:
            back()


def week_prompt():
    year = retryable_input("Enter year", lambda y: datetime_parser.parse_year(y), 3,
                           default=str(date.today().year)).year
    week = retryable_input("Enter week number", lambda w: datetime_parser.parse_week(w, year), 3,
                           default=str(date.today().isocalendar().week)).isocalendar().week
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
        printer.print_error("Deletion not confirmed, exiting.")
        exit()


def tpd_prompt(prompt_prefix: str, action: Callable[[date, time, time], None], back: Callable):
    options = ["[t] today", "[w] this week", "[d] any date", None, "[b] back"]
    terminal_menu = TerminalMenu(options, title=prompt_prefix)
    index = terminal_menu.show()

    match index:
        case 0:
            day = date.today()
            time_span_input(lambda starts_at, ends_at: action(day, starts_at, ends_at))
        case 1:
            weekday_prompt(prompt_prefix, action, lambda: tpd_prompt(prompt_prefix, action, back))
        case 2:
            date_prompt(prompt_prefix, action)
        case 4:
            back()


def weekday_prompt(prompt_prefix: str, action: Callable[[date, time, time], None], back: Callable):
    weekdays = list(map(lambda d: date.fromisocalendar(2024, 1, d).strftime("%A"), range(1, 8)))
    options = weekdays + [None, "[b] back"]
    terminal_menu = TerminalMenu(options, title="Choose a day")
    index = terminal_menu.show()
    match index:
        case None:
            return
        case 8:
            back()
        case i if 0 <= i < 7:
            today = date.today()
            day = datetime.strptime(weekdays[index] + "," + today.strftime("%W,%Y"), "%A,%W,%Y").date()
            printer.print_success(day.strftime(prompt_prefix + " entry for %A, %d %B %Y"))

            time_span_input(lambda starts_at, ends_at: action(day, starts_at, ends_at))


def date_prompt(prompt_prefix: str, action: Callable[[date, time, time], None]):
    day = retryable_input("Enter date (like YYYY-MM-DD)",
                          lambda date_str: datetime_parser.parse_date(date_str), 3)
    printer.print_success(day.strftime(prompt_prefix + " entry for %A, %d %B %Y"))

    time_span_input(lambda starts_at, ends_at: action(day, starts_at, ends_at))


def time_span_input[T](action: Callable[[time, time], T]) -> [T]:
    def after_time_input(time_span: str) -> None:
        starts_at, ends_at = datetime_parser.parse_time_span(time_span)
        action(starts_at, ends_at)

    retryable_input("Enter time span (like HH-HH or HH:mm-HH:mm)", after_time_input, 3)


def retryable_input[T](question: str, action: Callable[[str], T], retries: int, default: str = None, ) -> T:
    prompt = question
    if default:
        prompt = prompt + " (default {0})".format(default)

    for i in range(0, retries):
        user_input = console_input(prompt)
        try:
            if user_input == "":
                user_input = default
            return action(user_input)
        except ValueError as e:
            printer.print_error(str(e))
            prompt = "Try again: "

    printer.print_error("Failed to capture input")


def console_input(prompt: str) -> str:
    return printer.console.input("[bold red]> [/bold red]{0}: ".format(prompt))
