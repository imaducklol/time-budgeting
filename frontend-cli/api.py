"""
Author: Orion Hess
Created: 2025-12-11
Updated: 2025-12-11

Handle api calls
"""

from typing import Union, Any
import requests
from helpers import debug, error


class ApiHandler:
    def __init__(self, url: str, debug_mode: bool) -> None:
        self.url = url
        self.debug_mode = debug_mode

    def get_api(self, endpoint: str) -> Union[list[dict[str, Any]], dict[str, Any], None]:
        """
        Call GET method on the given endpoint with the given data

        :param endpoint: The endpoint to get from
        :return: Dictionary of json response
        """
        query = f"{self.url}/api/{endpoint}"
        debug(self.debug_mode, f"Querying: {query}")
        try:
            response = requests.get(query)
            debug(self.debug_mode, f"Response: {response}")
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                error(f"Endpoint {query} not found, returned 404")
            else:
                error(f"Something went wrong, returned {response.status_code}")
        except Exception:
            return None

    def post_api(self, endpoint: str, data: dict[str, str]) -> Union[dict[str, str], None]:
        """
        Call POST method on the given endpoint with the given data
        :param endpoint: the endpoint to post to
        :param data: the data to post
        :return: Dictionary of json response
        """
        query = f"{self.url}/api/{endpoint}"
        debug(self.debug_mode, f"Posting data to: {query}\nData: {data}")
        try:
            response = requests.post(query, json=data)
            debug(self.debug_mode, f"Response: {response}")
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 404:
                error(f"Endpoint {query} not found, returned 404")
            else:
                error(f"Something went wrong, returned {response.status_code}")
        except Exception as e:
            error(f"Something went wrong, errored with code {e}")

    def delete_api(self, endpoint: str) -> Union[dict[str, str], None]:
        """
        Call DELETE method on the given endpoint
        :param endpoint: the endpoint to delete
        :return: json response
        """
        query = f"{self.url}/api/{endpoint}"
        debug(self.debug_mode, f"Deleting: {query}")
        try:
            response = requests.delete(query)
            if response.status_code == 200:
                return response.json()
            elif response.status_code == 404:
                error(f"Endpoint {endpoint} not found, returned 404")
            else:
                error(f"Something went wrong, returned {response.status_code}")
        except Exception:
            return None

    def patch_api(self, endpoint: str, data: dict[str, str]) -> Union[dict[str, str], None]:
        """
        Call PATCH method on the given endpoint
        :param endpoint: The endpoint to update
        :param data: The data to send
        :return: Dictionary of json response
        """
        query = f"{self.url}/api/{endpoint}"
        debug(self.debug_mode, f"Updating: {query}\nData: {data}")
        try:
            response = requests.patch(query, json=data)
            if response.status_code == 201:
                return response.json()
            elif response.status_code == 404:
                error(f"Endpoint {endpoint} not found, returned 404")
            else:
                error(f"Something went wrong, returned {response.status_code}")
        except Exception:
            return None

    def push_api(self, endpoint: str, data):
        pass
