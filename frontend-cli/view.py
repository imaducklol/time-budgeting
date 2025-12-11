"""
Author: Orion Hess
Created: 2025-12-03
Updated: 2025-12-10

View handling the display of the cli frontend
"""
import os
import platform
import sys

import keyboard

from model import Model

if sys.platform == "win32":
    import msvcrt

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
                # Normalize behaviour of Enter key across Windows/Unix
                if ch == "\r": return "\n"
                return ch
        return None

else:
    import tty
    import termios
    import select


    def get_key():
        """Return a key press on Unix, or None if no key pressed."""
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(fd)
            # check if input is available
            if select.select([sys.stdin], [], [], 0)[0]:
                ch = sys.stdin.read(1)
                if ch == '\x1b':  # ESC
                    # Try to read the next two chars if available
                    if select.select([sys.stdin], [], [], 0)[0]:
                        ch2 = sys.stdin.read(1)
                        if ch2 == '[':
                            if select.select([sys.stdin], [], [], 0)[0]:
                                ch3 = sys.stdin.read(1)
                                if ch3 == 'A':
                                    return 'UP'
                                elif ch3 == 'B':
                                    return 'DOWN'
                                elif ch3 == 'C':
                                    return 'RIGHT'
                                elif ch3 == 'D':
                                    return 'LEFT'
                    return None  # lone escape or not a recognized arrow
                else:
                    return ch
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None


class Screen:

    def __init__(self, model: Model):
        self.model = model
        self._keymap = {}
        self._options = [
            {
                "label": "Space/Enter",
                "desc": "Select",
                "keys": [" ", "\n"],
                "func": self.model.select_item
            },
            {
                "label": "l/Right",
                "desc": "Edit",
                "keys": ["l", "RIGHT"],
                "func": self.model.edit_item
            },
            {
                "label": "j/Down",
                "desc": "Down",
                "keys": ["j", "DOWN"],
                "func": self.model.highlight_down
            },
            {
                "label": "k/Up",
                "desc": "Up",
                "keys": ["k", "UP"],
                "func": self.model.highlight_down
            },
        ]
        self.set_keymap()

    def set_keymap(self):
        self._keymap = {}
        for option in self._options:
            for key in option["keys"]:
                self._keymap[key] = option["func"]

    def display(self):
        pass

    def options(self) -> None:
        for option in self._options:
            print(f"{option["label"]} - {option["desc"]}")
        while True:
            key = get_key()
            if not key: continue
            if key in self._keymap:
                Screen.clear_console()
                self._keymap[key]()
                print()
                break

    @staticmethod
    def clear_console() -> None:
        """
        Check user OS and properly clear the screen
        """
        if platform.system() == "Windows":
            os.system("cls")  # Windows clear
        else:
            os.system("clear")  # Linux / macOS clear


class Login(Screen):
    def __init__(self, model: Model):
        super().__init__(model)
        self._options.append(
            {
            "label": "n",
            "desc": "New user",
            "keys": ["n"],
            "func": model.user_create,
            }
        )
        self.set_keymap()


    def display(self):
        print("You are not logged in")
        print("Please select a user")
        self.model.user_list()

class BudgetSelection(Screen):
    def __init__(self, model: Model):
        super().__init__(model)
        self._options.append(
            {
                "label": "n",
                "desc": "New budget",
                "keys": ["n"],
                "func": model.budget_create,
            }
        )
        self.set_keymap()

    def display(self):
        print(f"You are logged in as user {self.model.user_id}: {self.model.username}")
        print("Please select a budget")
        self.model.budget_list()

class Home(Screen):
    def __init__(self, model: Model):
        super().__init__(model)
        self._options.extend([
            {
                "label": "a",
                "desc": "Create category",
                "keys": ["a"],
                "func": model.category_create,
            },
            {
                "label": "s",
                "desc": "Create group",
                "keys": ["s"],
                "func": model.group_create,
            },
            {
                "label": "f",
                "desc": "Log transaction",
                "keys": ["f"],
                "func": model.transaction_create,
            }
        ])
        self.set_keymap()

    def display(self):
        print("¯\\_(ツ)_/¯")
        self.model.list()