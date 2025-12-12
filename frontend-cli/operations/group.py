"""
Author: Orion Hess
Created: 2025-12-11
Updated: 2025-12-11

Class for group interactions
"""

from typing import Any
from api import ApiHandler
from helpers import validate_choice, get_interval


class Group:
    def __init__(self, api_handler: ApiHandler) -> None:
        self.api_handler = api_handler

    def group_create(self, user_id, budget_id) -> None:
        """
        Prompt for and create a group
        """
        group_name = input("Group name: ")
        group = {"group_name": group_name}
        response = self.api_handler.post_api(f"users/{user_id}/budgets/{budget_id}/groups", group)

        self.up_to_date = False

    def group_update(self, user_id, budget_id, group_id) -> None:
        """
        Prompt for and update the given group
        :param group_id: Group to update
        """
        group_name = input("Updated group name: ")
        group = {"group_name": group_name}
        response = self.api_handler.patch_api(f"users/{user_id}/budgets/{budget_id}/groups/{group_id}", group)

    def group_delete(self, user_id, budget_id, group_id) -> None:
        """
        Prompt for and delete the given group
        :param group_id: The group to delete
        """
        if validate_choice("Are you sure you want to delete this group?"):
            response = self.api_handler.delete_api(f"users/{user_id}/budgets/{budget_id}/groups/{group_id}")

    def group_list(self):
        pass

    def group_info(self):
        pass
