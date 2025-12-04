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
            return msvcrt.getch().decode('utf-8')
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
                key = sys.stdin.read(1)
                return key
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return None


class Screen:

    def __init__(self, model: Model):
        self.model = model
        self._options = {}

    def display(self):
        pass

    def options(self) -> None:
        for option in self._options:
            print(f"{option} - {self._options[option]['desc']}")
        # user_input = input("selection: ")
        # print()
        # if user_input in self._options:
        #     self._options[user_input]['func']()
        # print()
        while True:
            key = get_key()
            if key in self._options:
                Screen.clear_console()
                self._options[key]['func']()
                print()
                break

    @staticmethod
    def clear_console():
        if platform.system() == "Windows":
            os.system("cls")  # Windows clear
        else:
            os.system("clear")  # Linux / macOS clear


class Login(Screen):
    def __init__(self, model: Model):
        super().__init__(model)
        self._options = {
            'l': {
                'desc': 'List users',
                'func': model.user_list
            },
            's': {
                'desc': 'Sign in',
                'func': model.sign_in
            },
            'c': {
                'desc': 'Create user',
                'func': model.user_create
            }
        }

    def display(self):
        print("You are not logged in")

class BudgetSelection(Screen):
    def __init__(self, model: Model):
        super().__init__(model)
        self._options = {
            's': {
                'desc': 'Select budget',
                'func': model.select_budget
            },
            'l': {
                'desc': 'Edit Item',
                'func': model.edit_item
            },
            'j': {
                'desc': 'Down',
                'func': model.highlight_down
            },
            'k': {
                'desc': 'Up',
                'func': model.highlight_up
            },
        }

    def display(self):
        print("You are logged in as user {model.user_id}: {model.username}")
        print("Please select a budget")
        self.model.budget_list()

class Home(Screen):
    def __init__(self, model: Model):
        super().__init__(model)
        self._options = {
            'l': {
                'desc': 'Edit Item',
                'func': model.edit_item
            },
            'j': {
                'desc': 'Down',
                'func': model.highlight_down
            },
            'k': {
                'desc': 'Up',
                'func': model.highlight_up
            },
            'a': {
                'desc': 'Create new category',
                'func': model.category_create
            },
            's': {
                'desc': 'Create new group',
                'func': model.group_create
            },
            'f': {
                'desc': 'Log new transaction',
                'func': model.transaction_create
            },

        }

    def display(self):
        print("")
