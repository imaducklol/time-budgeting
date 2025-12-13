"""
Author: Orion Hess
Created: 2025-12-11
Updated: 2022-12-11

Miscellaneous helper functions
"""

import os
import sys
from datetime import timedelta

import colorama
from colorama import init, Fore, Style
from tabulate import tabulate

colorama.init(autoreset=True)


def get_interval(message: str) -> timedelta:
    """
    Return a properly formatted interval for sql
    :param message: Message to display
    """
    print(message)
    days = int(input("Days: "))
    hours = int(input("Hours: "))
    minutes = int(input("Minutes: "))

    return timedelta(days=days, hours=hours, minutes=minutes)


def debug(debug_mode: bool, message: str) -> None:
    """
    Log a debug message if debug_mode is set
     :param message: Message to display
    """
    if debug_mode:
        for line in message.split("\n"):
            print(Fore.GREEN + f"DEBUG: {line}")


def error(message: str) -> None:
    """
    Log an error message
    :param message: Error message to display
    """
    for line in message.split("\n"):
        print(Fore.RED + f"ERROR: {line}")


def validate_choice(message: str) -> bool:
    """
    Validate the user's choice for a given option

    :param message: Question to validate
    :return: Boolean validated
    """
    print(message)
    response = input("y/N: ")
    return response.lower() == "y"


def print_dict(data: dict, headers: list[str], display_headers: list[str]) -> None:
    """
    Pretty print a dictionary

    :param data: Dictionary to be printed
    :param headers: Ordered dictionary keys
    :param display_headers: Ordered header alias
    :return: None
    """
    list = [[row[h] for h in headers] for row in data]
    print(tabulate(list, headers=display_headers, tablefmt="pipe"))


if sys.platform == "win32":
    def clear_console():
        os.system("cls")
else:
    def clear_console():
        os.system("clear")

from blessed import Terminal

term = Terminal()

def get_key():
    with term.cbreak():
        key = term.inkey(timeout=0.1)
        if not key:
            return None

        if key.name:
            return key.name  # 'KEY_UP', 'KEY_DOWN', 'KEY_LEFT', 'KEY_RIGHT'
        return str(key)