"""
Author: Orion Hess
Created: 2025-12-11
Updated: 2025-12-11

Class for user interactions
"""

from typing import Any
from api import ApiHandler
from helpers import validate_choice


class User:
    def __init__(self, api_handler: ApiHandler) -> None:
        self.api_handler = api_handler

    def user_create(self) -> None:
        """
        Prompt for user input and push to database
        """
        username = input("Username: ")
        email = input("Email: ")
        user = {'username': username, 'email': email}
        response = self.api_handler.post_api("users", user)

    def user_update(self, user_id) -> None:
        """
        Prompt for information and update the user with it
        """
        if validate_choice("Are you sure you want to update this user?"):
            username = input("New username: ")
            email = input("New email: ")
            response = self.api_handler.patch_api(f"users/{user_id}", {"username": username, "email": email})

    def user_delete(self, user_id: int) -> None:
        """
        Prompt for and delete a user
        """
        if validate_choice("Are you sure you want to delete this user?"):
            self.api_handler.delete_api(f"users/{user_id}")

    def user_list(self) -> list[dict[str, Any]]:
        """
        Print users to console
        """
        users = self.api_handler.get_api("users")
        return users

    def user_info(self) -> None:
        """
        Prompt for user ID and print respective info
        """
        id = int(input("User ID: "))
        user = self.api_handler.get_api(f"users/{id}")
        if user is None:
            return
        self.print_dict(
            data=user,
            headers=["user_id", "username", "email", "created_at"],
            display_headers=["ID", "Username", "Email", "Created"]
        )
