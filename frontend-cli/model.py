import requests
from tabulate import tabulate
import view
from typing import List, Tuple


class Model:
    user_id: int = None
    username: int = None
    email: int = None

    selected_budget: int = None

    selection_index: int = None
    display_items: List[Tuple[str, int]] = []

    def __init__(self, url):
        self.url = url

    def get_screen(self):
        if not self.user_id:
            return view.Login(self)
        if not self.selected_budget:
            return view.BudgetSelection(self)
        return view.Home(self)

    def get_api(self, endpoint: str):
        response = requests.get(f"{self.url}/api/{endpoint}")
        return response.json()

    def push_api(self, endpoint: str, data):
        pass

    def print_dict(self, data, headers, display_headers):
        list = [[row[h] for h in headers] for row in data]
        print(tabulate(list, headers=display_headers, tablefmt="pipe"))

    def highlight_up(self):
        if not self.selection_index:
            self.selection_index = 0
            return
        self.selection_index = (self.selection_index - 1) % len(self.display_items)

    def highlight_down(self):
        if not self.selection_index:
            self.selection_index = 0
            return
        self.selection_index = (self.selection_index + 1) % len(self.display_items)

    def select_item(self):
        match self.display_items[self.selection_index]:
            case ('budget', _):
                self.budget_info()
            case ('category', _):
                self.category_info()
            case ('group', _):
                self.group_info()
            case ('transaction', _):
                self.transaction_info()

    def edit_item(self):
        match self.display_items[self.selection_index]:
            case ('budget', _):
                self.budget_update()
            case ('category', _):
                self.category_update()
            case ('group', _):
                self.group_update()
            case ('transaction', _):
                self.transaction_update()



    ######################################################################
    # Login Page
    ######################################################################
    def sign_in(self):
        self.user_id = int(input("User ID: "))
        user = self.get_api(f"user/{self.user_id}")
        self.user_id = user["user_id"]
        self.username = user["username"]
        self.email = user["email"]

    ######################################################################
    # Select Budget Page
    ######################################################################
    def select_budget(self):
        _, self.selected_budget = self.display_items[self.selection_index]

    ######################################################################
    # Home Page
    ######################################################################

    ######################################################################
    # User
    ######################################################################
    def user_create(self):
        username = input("Username: ")
        email = input("Email: ")
        user = {'username': username, 'email': email}
        response = requests.post(f"{self.url}/api/user", json=user)
        print(response)

    def user_update(self):
        pass

    def user_delete(self):
        pass

    def user_list(self):
        users = self.get_api("user")
        self.print_dict(
            data = users,
            headers = ["user_id", "username", "email", "created_at"],
            display_headers = ["ID", "Username", "Email", "Created"]
        )

    def user_info(self):
        id = int(input("User ID: "))
        user = self.get_api(f"user/{id}")
        self.print_dict(
            data = user,
            headers = ["user_id", "username", "email", "created_at"],
            display_headers = ["ID", "Username", "Email", "Created"]
        )

    ######################################################################
    # Budget
    ######################################################################
    def budget_create(self):
        pass

    def budget_update(self):
        pass

    def budget_delete(self):
        pass

    def budget_list(self, user_id: int = user_id):
        budgets = self.get_api(f"budget/{user_id}")
        self.print_dict(
            data = budgets,
            headers = ["budget_id", "budget_name", "budget_description"],
            display_headers = ["ID", "Budget Name", "Budget Description"]
        )

    def budget_info(self):
        pass

    ######################################################################
    # Category
    ######################################################################
    def category_create(self):
        pass

    def category_update(self):
        pass

    def category_delete(self):
        pass

    def category_list(self):
        pass

    def category_info(self):
        pass

    ######################################################################
    # Group
    ######################################################################
    def group_create(self):
        pass

    def group_update(self):
        pass

    def group_delete(self):
        pass

    def group_list(self):
        pass

    def group_info(self):
        pass

    ######################################################################
    # Transaction
    ######################################################################
    def transaction_create(self):
        pass

    def transaction_update(self):
        pass

    def transaction_delete(self):
        pass

    def transaction_list(self):
        pass

    def transaction_info(self):
        pass
