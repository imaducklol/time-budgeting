"""
Author: Orion Hess
Created: 2025-12-03
Updated: 2025-12-11

Model handling the logic of the cli frontend
"""

import colorama
from colorama import init, Fore, Style

import view
from api import ApiHandler
from helpers import debug
from operations.user import User
from operations.budget import Budget
from operations.category import Category
from operations.group import Group
from operations.transaction import Transaction

colorama.init(autoreset=True)


class Model:
    # Login data
    user_id: int | None = None
    username: str | None = None
    email: int | None = None

    # Is an item selected?
    selected_budget: int | None = None
    selected_category: int | None = None
    selected_group: int | None = None

    # Items available for selection/display
    selection_index: int = None
    display_items: list[tuple[str, int, str]] = []

    up_to_date: bool = False

    def __init__(self, url: str, debug_mode: bool = True) -> None:
        self.url = url
        self.debug_mode = debug_mode

        self.api_handler = ApiHandler(self.url, self.debug_mode)
        self.user = User(self.api_handler)
        self.budget = Budget(self.api_handler)
        self.category = Category(self.api_handler)
        self.group = Group(self.api_handler)
        self.transaction = Transaction(self.api_handler)

    def get_screen(self):
        if not self.user_id:
            debug(self.debug_mode, "Login Screen")
            return view.Login(self)
        if not self.selected_budget:
            debug(self.debug_mode, "Budget Screen")
            return view.BudgetSelection(self)
        # if self.selected_category:
        #    debug(self.debug_mode, "Category Screen")
        #    return view.CategorySelected(self)
        # if self.selected_group:
        #    debug(self.debug_mode, "Group Screen")
        #    return view.GroupSelected(self)
        debug(self.debug_mode, "Home Screen")
        return view.Home(self)

    def highlight_up(self):
        # If there are no items, keep index None
        if len(self.display_items) == 0:
            return
        # If unset, go to bottom
        if self.selection_index is None:
            self.selection_index = len(self.display_items) - 1
            return
        self.selection_index = (self.selection_index - 1) % len(self.display_items)

    def highlight_down(self):
        # If there are no items, keep index None
        if len(self.display_items) == 0:
            return
        # If unset, go to top
        if self.selection_index is None:
            self.selection_index = 0
            return
        self.selection_index = (self.selection_index + 1) % len(self.display_items)

    def validate_index(self) -> bool:
        """
        Make sure that the selected index is valid
        :return: True if valid, False otherwise
        """
        # If we have not moved the cursor to anything, select the first
        if self.selection_index is None:
            self.selection_index = 0
            return False
        # If the list is empty, pass
        if len(self.display_items) == 0:
            return False
        # If the index is out of bounds, fix
        if (self.selection_index < 0 or self.selection_index >= len(self.display_items)):
            self.selection_index = 0
            return False
        return True

    def select_item(self) -> None:
        if not self.validate_index():
            return

        # Depending on what type of item we have selected, do something
        match self.display_items[self.selection_index]:
            case ('user', x, y):
                self.user_id = x
                self.username = y
                self.up_to_date = False
            case ('budget', x, _):
                self.selected_budget = x
                self.up_to_date = False
            case ('category', x, _):
                self.selected_category = x
                self.up_to_date = False
            case ('group', x, _):
                self.selected_group = x
                self.up_to_date = False
            # case ('transaction', x, _):
            #     self.up_to_date = False
            case _:
                return
                # raise Exception(f"Invalid selection: {self.display_items[self.selection_index]}")

    def edit_item(self):
        self.validate_index()

        # Depending on what type of item we want to edit, do something
        match self.display_items[self.selection_index]:
            case ('user', x, _):
                self.user.user_update(x)
            case ('budget', x, _):
                self.budget.budget_update(self.user_id, x)
            case ('category', x, _):
                self.category.category_update(self.user_id, self.selected_budget, x)
            case ('group', x, _):
                self.group.group_update(self.user_id, self.selected_budget, x)
            case ('transaction', x, _):
                self.transaction.transaction_update(self.user_id, self.selected_budget, x)
            case _:
                raise Exception(f"Invalid selection: {self.display_items[self.selection_index]}")

    def delete_item(self):
        self.validate_index()

        self.up_to_date = False

        match self.display_items[self.selection_index]:
            case ('user', x, _):
                self.user.user_delete(x)
            case ('budget', x, _):
                self.budget.budget_delete(self.user_id, x)
            case ('category', x, _):
                self.category.category_delete(self.user_id, self.selected_budget, x)
            case ('group', x, _):
                self.group.group_delete(self.user_id, self.selected_budget, x)
            case ('transaction', x, _):
                self.transaction.transaction_delete(self.user_id, self.selected_budget, x)
            case _:
                raise Exception(f"Invalid selection: {self.display_items[self.selection_index]}")

    def back(self) -> None:
        """
        Go back a page by unsetting the relevant variable
        """
        debug(self.debug_mode, f"Back called")
        self.up_to_date = False
        if self.selected_category is not None:
            self.selected_category = None
            return
        if self.selected_group is not None:
            self.selected_group = None
            return
        if self.selected_budget is not None:
            self.selected_budget = None
            return
        if self.user_id is not None:
            self.user_id = None
            return

    def validate_user_budget(self) -> None:
        if not self.user_id: raise Exception("Called general list without user_id set")
        if not self.selected_budget: raise Exception("Called general list without budget_id set")

    def list(self) -> None:
        """
        List groups and categories within a budget
        """
        if not self.up_to_date:
            if self.user_id is None:
                users = self.user.user_list()
                self.display_items.clear()
                if users:
                    self.display_items = [
                        ("user", u["user_id"], u["username"] + " - " + u["email"]) for u in users
                    ]
                    self.up_to_date = True
            elif self.selected_budget is None:
                budgets = self.budget.budget_list(self.user_id)
                self.display_items.clear()
                if budgets:
                    self.display_items = [
                        ("budget", b["budget_id"], b["budget_name"]) for b in budgets
                    ]
                    self.up_to_date = True
            elif self.selected_group is not None:
                categories = self.category.category_list(
                    self.user_id,
                    self.selected_budget,
                    self.selected_group
                )
                self.display_items.clear()
                if categories:
                    self.display_items = [
                        ("category", c["category_id"], c["category_name"]) for c in categories
                    ]
                    self.up_to_date = True
            elif self.selected_category is not None:
                transactions = self.transaction.transaction_list(
                    self.user_id,
                    self.selected_budget,
                    self.selected_category
                )
                self.display_items.clear()
                if transactions:
                    self.display_items = [
                        ("transaction", t["transaction_id"], t["transaction_name"]) for t in transactions
                    ]
                    self.up_to_date = True
            else:
                self.list_categories_and_groups()
                self.up_to_date = True

        ungrouped = True
        for index, item in enumerate(self.display_items):
            # Display selected item
            if index == self.selection_index:
                print(" -> ", end="")
            else:
                print("    ", end="")

            if item[0] == "group":
                ungrouped = False
                print(Fore.LIGHTBLACK_EX + f"{item[2]}")
            elif item[0] == "category":
                # Tab in categories for distinction from groups
                if not ungrouped: print("  ", end="")
                print(Fore.LIGHTCYAN_EX + f"{item[2]}")
            print(Fore.LIGHTGREEN_EX + f"{item[2]}")

    def list_categories_and_groups(self) -> None:
        self.validate_user_budget()
        categories = self.api_handler.get_api(f"users/{self.user_id}/budgets/{self.selected_budget}/categories")
        groups = self.api_handler.get_api(f"users/{self.user_id}/budgets/{self.selected_budget}/groups")

        if categories is None or groups is None:
            return

        self.display_items.clear()

        grouped = {}
        ungrouped = []

        for c in categories:
            group_id = c["group_id"]
            if group_id is None:
                ungrouped.append(("category", c["category_id"], c["category_name"]))
            else:
                if group_id not in grouped:
                    grouped[group_id] = []
                grouped[group_id].append(("category", c["category_id"], c["category_name"]))

        self.display_items.extend(ungrouped)

        for g in groups:
            self.display_items.append(("group", g["group_id"], g["group_name"]))

            if g["group_id"] in grouped.keys():
                self.display_items.extend(grouped[g["group_id"]])

    def user_create(self) -> None:
        self.user.user_create()
        self.up_to_date = False

    def budget_create(self) -> None:
        if self.user_id is None:
            return
        self.budget.budget_create(self.user_id)
        self.up_to_date = False

    def category_create(self) -> None:
        self.validate_user_budget()
        self.category.category_create(self.user_id, self.selected_budget)
        self.up_to_date = False

    def group_create(self) -> None:
        self.validate_user_budget()
        self.group.group_create(self.user_id, self.selected_budget)
        self.up_to_date = False

    def transaction_create(self) -> None:
        self.validate_user_budget()
        self.transaction.transaction_create(self.user_id, self.selected_budget)
        self.up_to_date = False
