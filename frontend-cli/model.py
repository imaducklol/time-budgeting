"""
Author: Orion Hess
Created: 2025-12-03
Updated: 2025-12-10

Model handling the logic of the cli frontend
"""
import colorama
import requests
from tabulate import tabulate
from colorama import init, Fore, Style
import view
from typing import Union, Any

class Model:
    debug_mode = True

    # Login data
    user_id: int = None
    username: int = None
    email: int = None

    # Is an item selected?
    selected_budget: int = None
    selected_category: int = None
    selected_group: int = None

    # Items available for selection/display
    selection_index: int = None
    display_items: list[tuple[str, int, str]] = []

    up_to_date: bool = False

    def __init__(self, url):
        self.url = url

        colorama.init(autoreset=True)

    def get_screen(self):
        if not self.user_id:
            self.debug("Login Screen")
            return view.Login(self)
        if not self.selected_budget:
            self.debug("Budget Screen")
            return view.BudgetSelection(self)
        if self.selected_category:
            self.debug("Category Screen")
            return view.CategorySelected(self)
        if self.selected_group:
            self.debug("Group Screen")
            return view.GroupSelected(self)
        self.debug("Home Screen")
        return view.Home(self)

    def get_api(self, endpoint: str) -> Union[list[dict[str, Any]], dict[str, Any]]:
        """
        Call GET method on the given endpoint with the given data

        :param endpoint: The endpoint to get from
        :return: Dictionary of json response
        """
        query = f"{self.url}/api/{endpoint}"
        self.debug(f"Querying: {query}")
        response = requests.get(query)
        self.debug(f"Response: {response}")
        if response.status_code == 404:
            raise Exception(f"Endpoint {endpoint} not found, returned 404")
        return response.json()

    def post_api(self, endpoint: str, data: dict[str, str]) -> dict[str, str]:
        """
        Call POST method on the given endpoint with the given data
        :param endpoint: the endpoint to post to
        :param data: the data to post
        :return: Dictionary of json response
        """
        query = f"{self.url}/api/{endpoint}"
        self.debug(f"Posting data: {data}\nData: {query}")
        response = requests.post(query, json=data)
        self.debug(f"Response: {response}")
        if response.status_code == 404:
            raise Exception(f"Endpoint {endpoint} not found, returned 404")
        return response.json()

    def delete_api(self, endpoint: str) -> dict[str, str]:
        """
        Call DELETE method on the given endpoint
        :param endpoint: the endpoint to delete
        :return: json response
        """
        query = f"{self.url}/api/{endpoint}"
        self.debug(f"Deleting: {query}")
        response = requests.delete(query)
        if response.status_code == 404:
            raise Exception(f"Endpoint {endpoint} not found, returned 404")
        return response.json()

    def patch_api(self, endpoint: str, data: dict[str, str]) -> dict[str, str]:
        """
        Call PATCH method on the given endpoint
        :param endpoint: The endpoint to update
        :param data: The data to send
        :return: Dictionary of json response
        """
        query = f"{self.url}/api/{endpoint}"
        self.debug(f"Updating: {query}\nData: {data}")
        response = requests.patch(query, json=data)
        if response.status_code == 404:
            raise Exception(f"Endpoint {endpoint} not found, returned 404")
        return response.json()

    def push_api(self, endpoint: str, data):
        pass

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

    def select_item(self) -> None:
        # If we have not moved the cursor to anything, select the first
        if self.selection_index is None:
            self.selection_index = 0
            return
        # If the list is empty, pass
        if len(self.display_items) == 0:
            return
        # If the index is out of bounds, raise
        if (self.selection_index < 0 or self.selection_index >= len(self.display_items)):
            raise Exception(f"Selection index was out of bounds,"
                            "this should never happen...")
        # Depending on what type of item we have selected, do something
        match self.display_items[self.selection_index]:
            case ('user', x, _):
                self.user_id = x
                # TODO Get username
                self.up_to_date = False
                #self.user_info()
            case ('budget', x, _):
                self.selected_budget = x
                self.up_to_date = False
                #self.budget_info()
            case ('category', x, _):
                self.selected_category = x
                self.category_info()
            case ('group', x, _):
                self.selected_group = x
                self.group_info()
            case ('transaction', x, _):
                self.transaction_info()
            case _:
                raise Exception(f"Invalid selection: {self.display_items[self.selection_index]}")

    def edit_item(self):
        # If we have not moved the cursor to anything, select the first
        if self.selection_index is None:
            self.selection_index = 0
            return

        # Depending on what type of item we want to edit, do something
        match self.display_items[self.selection_index]:
            case ('budget', _):
                self.budget_update()
            case ('category', _):
                self.category_update()
            case ('group', _):
                self.group_update()
            case ('transaction', _):
                self.transaction_update()

    def validate_choice(self, message: str) -> bool:
        """
        Validate the user's choice for a given option

        :param message: Question to validate
        :return: Boolean validated
        """
        print(message)
        response = input("y/N: ")
        return response.lower() == "y"

    def print_dict(self, data: dict, headers: list[str], display_headers: list[str]) -> None:
        """
        Pretty print a dictionary

        :param data: Dictionary to be printed
        :param headers: Ordered dictionary keys
        :param display_headers: Ordered header alias
        :return: None
        """
        list = [[row[h] for h in headers] for row in data]
        print(tabulate(list, headers=display_headers, tablefmt="pipe"))

    def debug(self, message: str) -> None:
        """
        Log a debug message if debug_mode is set

        :param message: Message to display
        """
        if self.debug_mode:
            for line in message.split("\n"):
                print(Fore.GREEN + f"DEBUG: {line}")

    def validate_user_budget(self) -> None:
        if not self.user_id: raise Exception("Called general list without user_id set")
        if not self.selected_budget: raise Exception("Called general list without budget_id set")

    def list(self) -> None:
        """
        List groups and categories within a budget
        """
        if not self.up_to_date:
            self.validate_user_budget()
            categories = self.get_api(f"users/{self.user_id}/budgets/{self.selected_budget}/categories")
            groups = self.get_api(f"users/{self.user_id}/budgets/{self.selected_budget}/groups")

            self.display_items.clear()
            for group in groups:
                self.display_items.append(('group', int(group["group_id"]), group["group_name"]))

            ungrouped = []
            for index, item in enumerate(self.display_items):
                for c in categories:
                    if c["group_id"] == item:
                        self.display_items.insert(index, ("category", c["category_id"], c["category_name"]))
                    else:
                        ungrouped.append(("category", c["category_id"], c["category_name"]))

            self.display_items = ungrouped + self.display_items

        for index, item in enumerate(self.display_items):
            # Display selected item
            if index == self.selection_index: print(" -> ", end="")
            else: print("    ", end="")
            # Tab in categories for distinction from groups
            if item[0] == "category": print("  ", end="")

            print(f"{item[0]} - {item[1]}: {item[2]}")

    ######################################################################
    # Login Page
    ######################################################################
    def sign_in(self) -> None:
        """
        Ask for and set a user id, triggering the choose budget page
        """
        self.user_id = int(input("User ID: "))
        user = self.get_api(f"users/{self.user_id}")
        self.user_id = user["user_id"]
        self.username = user["username"]
        self.email = user["email"]

    ######################################################################
    # Select Budget Page
    ######################################################################

    ######################################################################
    # Home Page
    ######################################################################

    ######################################################################
    # User
    ######################################################################
    def user_create(self) -> None:
        """
        Prompt for user input and push to database
        """
        username = input("Username: ")
        email = input("Email: ")
        user = {'username': username, 'email': email}
        response = self.post_api("users", user)

        self.up_to_date = False

    def user_update(self) -> None:
        """
        Prompt for information and update the user with it
        """
        if self.validate_choice("Are you sure you want to update this user?"):
            username = input("New username: ")
            email = input("New email: ")
            self.patch_api(f"users/{self.user_id}", {"username": username, "email": email})

    def user_delete(self) -> None:
        """
        Prompt for and delete a user
        """
        if self.validate_choice("Are you sure you want to delete this user?"):
            self.delete_api(f"users/{self.user_id}")

    def user_list(self) -> None:
        """
        Print users to console
        """
        if not self.up_to_date:
            self.up_to_date = True
            users = self.get_api("users")

            # Update the displayed items for use in selection
            self.display_items.clear()
            for user in users:
                self.display_items.append(('user', user["user_id"], user["username"] + " - " + user["email"]))

        self.list()
        #self.print_dict(
        #    data = users,
        #    headers = ["user_id", "username", "email", "created_at"],
        #    display_headers = ["ID", "Username", "Email", "Created"]
        #)

    def user_info(self) -> None:
        """
        Prompt for user ID and print respective info
        """
        id = int(input("User ID: "))
        user = self.get_api(f"users/{id}")
        self.print_dict(
            data = user,
            headers = ["user_id", "username", "email", "created_at"],
            display_headers = ["ID", "Username", "Email", "Created"]
        )

    ######################################################################
    # Budget
    ######################################################################
    def budget_create(self) -> None:
        """
        Prompt for and create a budget
        """
        self.debug("Entered budget_create")
        budget_name = input("Budget Name: ")
        budget_description = input("Budget Description: ")
        budget = {"budget_name": budget_name, "budget_description": budget_description}
        response = self.post_api(f"users/{self.user_id}/budgets", budget)

        self.up_to_date = False

    def budget_update(self) -> None:
        """
        Prompt for and update selected budget
        """
        budget_name = input("Updated budget name: ")
        budget_description = input("Updated budget description: ")
        budget = {"budget_name": budget_name, "budget_description": budget_description}
        response = self.patch_api(f"users/{self.user_id}/budgets/{self.selected_budget}", budget)

    def budget_delete(self) -> None:
        """
        Validate then delete selected budget
        """
        if self.validate_choice("Are you sure you want to delete this budget?"):
            self.delete_api(f"/api/{self.user_id}/budgets/{self.selected_budget}")

    def budget_list(self) -> None:
        """Get budgets to print and add to display_items"""
        if not self.up_to_date:
            self.up_to_date = True
            budgets = self.get_api(f"users/{self.user_id}/budgets")

            # Update the displayed items for use in selection
            self.display_items.clear()
            for budget in budgets:
                self.display_items.append(('budget', budget["budget_id"], budget["budget_name"]))

        self.list()
        # Pretty print dictionary to UI
        #self.print_dict(
        #    data = budgets,
        #    headers = ["budget_id", "budget_name", "budget_description"],
        #    display_headers = ["ID", "Budget Name", "Budget Description"]
        #)

    def budget_info(self):
        pass

    ######################################################################
    # Category
    ######################################################################
    def category_create(self) -> None:
        """
        Prompt for and create a new category
        """
        name = input("Category Name: ")
        time_allocated = self.get_time("Time Allocated: ")
        category = {"category_name": name, "time_allocated": time_allocated}
        response = self.post_api(f"users/{self.user_id}/budgets/{self.selected_budget}/categories", category)

        self.up_to_date = False

    def category_update(self, category_id: int) -> None:
        """
        Prompt for and update the given category
        :param category_id: The category to update
        """
        category_name = input("Updated category name: ")
        time_allocated = input("Updated time allocated: ")
        category = {"category_name": category_name, "time_allocated": time_allocated}
        response = self.patch_api(f"users/{self.user_id}/budgets/{self.selected_budget}/categories/{category_id}", category)

    def category_delete(self, category_id: int) -> None:
        """
        Prompt for and delete the given category
        :param category_id: Category to delete
        """
        if self.validate_choice("Are you sure you want to delete this category?"):
            response = self.delete_api(f"users/{self.user_id}/budgets/{self.selected_budget}/categories/{category_id}")

    def category_list(self) -> None:
        pass

    def category_info(self):
        pass

    ######################################################################
    # Group
    ######################################################################
    def group_create(self) -> None:
        """
        Prompt for and create a group
        """
        group_name = input("Group name: ")
        group = {"group_name": group_name}
        response = self.post_api(f"users/{self.user_id}/budgets/{self.selected_budget}/groups", group)

        self.up_to_date = False

    def group_update(self, group_id) -> None:
        """
        Prompt for and update the given group
        :param group_id: Group to update
        """
        group_name = input("Updated group name: ")
        group = {"group_name": group_name}
        response = self.post_api(f"users/{self.user_id}/budgets/{self.selected_budget}/groups/{group_id}", group)

    def group_delete(self, group_id) -> None:
        """
        Prompt for and delete the given group
        :param group_id: The group to delete
        """
        if self.validate_choice("Are you sure you want to delete this group?"):
            response = self.delete_api(f"users/{self.user_id}/budgets/{self.selected_budget}/groups/{group_id}")

    def group_list(self):
        pass

    def group_info(self):
        pass

    ######################################################################
    # Transaction
    ######################################################################
    def transaction_create(self):
        """
        Prompt for and create a transaction
        """
        transaction_name = input("Transaction name: ")
        period = self.get_time("Period: ")
        group_id = self.selected_group
        transaction = {"transaction_name": transaction_name, "period": period, "group_id": group_id}
        response = self.post_api(f"users/{self.user_id}/budgets/{self.selected_budget}/transactions", transaction)

        # TODO Do we need to unset up_to_date?

    def transaction_update(self, transaction_id) -> None:
        """
        Prompt for and update the given transaction
        :param transaction_id: The transaction to update
        """
        transaction_name = input("Updated transaction name: ")
        period = self.get_time("Updated period: ")
        group_id = self.selected_group
        transaction = {"transaction_name": transaction_name, "period": period, "group_id": group_id}
        response = self.patch_api(f"users/{self.user_id}/budgets/{self.selected_budget}/transactions/{transaction_id}", transaction)

    def transaction_delete(self, transaction_id) -> None:
        """
        Prompt for and delete the given transaction
        :param transaction_id: The transaction to delete
        """
        if self.validate_choice("Are you sure you want to delete this transaction?"):
            response = self.delete_api(f"users/{self.user_id}/budgets/{self.selected_budget}/transactions/{transaction_id}")

    def transaction_list(self):
        pass

    def transaction_info(self):
        pass
