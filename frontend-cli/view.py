"""
Author: Orion Hess
Created: 2025-12-03
Updated: 2025-12-11

View handling the display of the cli frontend
"""

from model import Model
from helpers import clear_console, get_key


class Screen:

    def __init__(self, model: Model):
        self.model = model
        self._keymap = {}
        self._options = [
            {
                "label": "k/↑ ",
                "desc": "Up",
                "keys": ["k", "KEY_UP"],
                "func": self.model.highlight_up
            },
            {
                "label": "j/↓",
                "desc": "Down",
                "keys": ["j", "KEY_DOWN"],
                "func": self.model.highlight_down
            },
            {
                "label": "⎋/←",
                "desc": "Back",
                "keys": ["ESC", "KEY_LEFT"],
                "func": self.model.back
            },
            {
                "label": "l/→",
                "desc": "Edit",
                "keys": ["l", "KEY_RIGHT"],
                "func": self.model.edit_item
            },
            {
                "label": "␣/↩",
                "desc": "Select",
                "keys": [" ", "KEY_ENTER"],
                "func": self.model.select_item
            },
            {
                "label": "d",
                "desc": "Delete",
                "keys": ["d"],
                "func": self.model.delete_item
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
        print()
        for option in self._options:
            print(f"{option["label"]:15} {option["desc"]}")
        while True:
            key = get_key()
            if not key: continue
            print(key)
            if key in self._keymap:
                clear_console()
                self._keymap[key]()
                print()
                break


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
        self.model.list()


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
        self.model.list()


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
