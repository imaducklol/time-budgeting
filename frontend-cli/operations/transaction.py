"""
Author: Orion Hess
Created: 2025-12-11
Updated: 2025-12-11

Class for transaction interactions
"""

from typing import Any
from unicodedata import category

from api import ApiHandler
from helpers import validate_choice, get_interval


class Transaction:
    def __init__(self, api_handler: ApiHandler) -> None:
        self.api_handler = api_handler

    def transaction_create(self, user_id, budget_id, category_id):
        """
        Prompt for and create a transaction
        """
        transaction_name = input("Transaction name: ")
        period = get_interval("Period: ").total_seconds()
        print(period)

        transaction = {"transaction_name": transaction_name, "period": period, }
        response = self.api_handler.post_api(f"users/{user_id}/budgets/{budget_id}/categories/{category_id}/transactions", transaction)

        # TODO Do we need to unset up_to_date?

    def transaction_update(self, user_id, budget_id, category_id, transaction_id) -> None:
        """
        Prompt for and update the given transaction
        :param transaction_id: The transaction to update
        """
        transaction_name = input("Updated transaction name: ")
        period = get_interval("Updated period: ").total_seconds()
        transaction = {"transaction_name": transaction_name, "period": period, }
        response = self.api_handler.patch_api(f"users/{user_id}/budgets/{budget_id}/categories/{category_id}/transactions/{transaction_id}",
                                              transaction)

    def transaction_delete(self, user_id, budget_id, category_id, transaction_id) -> None:
        """
        Prompt for and delete the given transaction
        :param transaction_id: The transaction to delete
        """
        if validate_choice("Are you sure you want to delete this transaction?"):
            response = self.api_handler.delete_api(f"users/{user_id}/budgets/{budget_id}/categories/{category_id}/transactions/{transaction_id}")

    def transaction_list(self, user_id, budget_id, category_id) -> list[dict[str, Any]] | None:
        response = self.api_handler.get_api(
            f"users/{user_id}/budgets/{budget_id}/categories/{category_id}/transactions")
        return response

    def transaction_info(self):
        pass
