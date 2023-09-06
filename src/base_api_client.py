# -*- coding: utf-8 -*-
from abc import ABC, abstractmethod
from typing import Any, List, Dict


class BaseAPIClient(ABC):
    """
    Client for interacting with the API provided by dummyapi.io service.
    """

    def __init__(self, url: str, auth_header: dict[str, Any]) -> None:
        self.home_url = url
        self.header = auth_header

        # Check connectivity during class construction
        self.check_connection()

    @abstractmethod
    def check_connection(self) -> None:
        """
        Abstract method meant for checking connection
        """

    @abstractmethod
    def get_users(self) -> List[Dict[str, Any]]:
        """
        Retrieve a list of users from the API.
        """

    @abstractmethod
    def get_posts_with_comments(self) -> List[Dict[str, Any]]:
        """
        Retrieve a list of posts with comments from the API.
        """
