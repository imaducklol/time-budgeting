"""
Author: Orion Hess
Created: 2025-12-11
Updated: 2025-12-11

Class for category interactions
"""

from typing import Any
from api import ApiHandler
from helpers import validate_choice, get_interval


class Category:
    def __init__(self, api_handler: ApiHandler) -> None:
        self.api_handler = api_handler

    def category_create(self, user_id, budget_id) -> None:
        """
        Prompt for and create a new category
        """
        name = input("Category Name: ")
        time_allocated = get_interval("Time Allocated").seconds
        category = {"category_name": name, "time_allocated": time_allocated}
        response = self.api_handler.post_api(f"users/{user_id}/budgets/{budget_id}/categories", category)

    def category_update(self, user_id, budget_id, category_id: int) -> None:
        """
        Prompt for and update the given category
        :param category_id: The category to update
        """
        category_name = input("Updated category name: ")
        time_allocated = input("Updated time allocated: ")
        category = {"category_name": category_name, "time_allocated": time_allocated}
        response = self.api_handler.patch_api(f"users/{user_id}/budgets/{budget_id}/categories/{category_id}", category)

    def category_delete(self, user_id, budget_id, category_id: int) -> None:
        """
        Prompt for and delete the given category
        :param category_id: Category to delete
        """
        if validate_choice("Are you sure you want to delete this category?"):
            response = self.api_handler.delete_api(f"users/{user_id}/budgets/{budget_id}/categories/{category_id}")

    def category_list(self, user_id, budget_id, group_id=None) -> list[dict[str, Any]] | None:
        """
        Return a list of categories
        :return: List of categories
        """
        if group_id is None:
            response = self.api_handler.get_api(f"users/{user_id}/budgets/{budget_id}/categories")
        else:
            response = self.api_handler.get_api(f"users/{user_id}/budget/{budget_id}/groups/{group_id}/categories")
        return response

    def category_info(self):
        pass
