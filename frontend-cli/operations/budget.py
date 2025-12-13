"""
Author: Orion Hess
Created: 2025-12-11
Updated: 2025-12-11

Class for budget interactions
"""

from typing import Any
from api import ApiHandler
from helpers import validate_choice


class Budget:
    def __init__(self, api_handler: ApiHandler) -> None:
        self.api_handler = api_handler

    def budget_create(self, user_id) -> None:
        """
        Prompt for and create a budget
        """
        budget_name = input("Budget Name: ")
        budget = {"budget_name": budget_name}
        response = self.api_handler.post_api(f"users/{user_id}/budgets", budget)

        self.up_to_date = False

    def budget_update(self, user_id, budget_id: int) -> None:
        """
        Prompt for and update selected budget
        """
        budget_name = input("Updated budget name: ")
        budget = {
            "budget_name": budget_name,
        }
        response = self.api_handler.patch_api(
            f"users/{user_id}/budgets/{budget_id}", budget
        )

    def budget_delete(self, user_id, budget_id) -> None:
        """
        Validate then delete selected budget
        """
        if validate_choice("Are you sure you want to delete this budget?"):
            self.api_handler.delete_api(f"users/{user_id}/budgets/{budget_id}")

    def budget_list(self, user_id) -> list[dict[str, Any]]:
        """Get budgets to print and add to display_items"""
        budgets = self.api_handler.get_api(f"users/{user_id}/budgets")
        return budgets

    def budget_info(self):
        pass
