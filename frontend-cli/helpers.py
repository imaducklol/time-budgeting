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
    import msvcrt


    def clear_console():
        os.system("cls")


    def get_key():
        """Return a key press on Windows, or None if no key pressed."""
        if msvcrt.kbhit():
            first = msvcrt.getch()
            # Arrow key codes begin with these escape strings
            if first in (b"\x00", b"\xe0"):
                second = msvcrt.getch().decode()
                match second:
                    case "H":
                        return "UP"
                    case "P":
                        return "DOWN"
                    case "K":
                        return "LEFT"
                    case "M":
                        return "RIGHT"
            else:
                # If not fancy, just decode it
                ch = first.decode("utf-8")
                # Normalize behaviour of certain keys across Windows/Unix
                if ch == "\r": return "\n"
                if ch == "\x0b": return "ESC"
                return ch
        return None

else:
    import tty
    import termios
    import select


    def clear_console():
        os.system("clear")


    def get_key():
        """Return a key press on Unix, or None if no key pressed."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # check if input is available
            if select.select([sys.stdin], [], [], 0)[0]:
                ch = sys.stdin.read(1)
                if ch == "\x1b":  # ESC
                    # Try to read the next two chars if available
                    if select.select([sys.stdin], [], [], 0)[0]:
                        ch1 = sys.stdin.read(1)
                        if ch1 == "[":
                            if select.select([sys.stdin], [], [], 0)[0]:
                                ch2 = sys.stdin.read(1)
                                if ch2 == "A":
                                    return "UP"
                                elif ch2 == "B":
                                    return "DOWN"
                                elif ch2 == "C":
                                    return "RIGHT"
                                elif ch2 == "D":
                                    return "LEFT"
                    return "ESC"
                else:
                    return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None
