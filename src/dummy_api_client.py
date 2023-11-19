# -*- coding: utf-8 -*-
from typing import List, Dict, Any, Generator
import requests  # type: ignore
from src.base_api_client import BaseAPIClient
import src.error_classes as error


class DummyAPIClient(BaseAPIClient):
    """
    Client for interacting with the API provided by dummyapi.io service.
    """

    def check_connection(self) -> None:
        """
        Check the connection to the API.

        Raises:
            ValueError: If an invalid token is provided.
            ValueError: If no token is provided.
            Exception: If there is a failure to cpip install pre-commit
        onnect to the API.
        """
        url = f"{self.home_url}/user"
        response = requests.get(url, headers=self.header, timeout=5)
        if response.status_code == 200:
            return

        if response.status_code == 403:
            error_data = response.json().get("error", {})
            if error_data == "APP_ID_NOT_EXIST":
                raise error.InvalidTokenError()
            if error_data == "APP_ID_MISSING":
                raise error.MissingTokenError()

        if response.status_code == 404:
            raise error.ServerDoesNotRespondError()

        raise error.APIConnectionError()

    def _paginate(
        self, url: str, params: dict[str, int] | None, page_limit: int = 10
    ) -> Generator[Dict[str, Any], None, None]:
        """
        Paginate through the API responses to retrieve all data.

        Args:
            url (str): The base URL for the API endpoint.
            params (dict, optional): Additional query parameters.
            Defaults to None.

        Returns:
            list: List of data objects retrieved from paginated API responses.
        """
        all_data: List[Any] = []
        page_count = 0
        num_of_records = 0

        while True:
            response = requests.get(url, headers=self.header, params=params, timeout=5)
            response_data = response.json()

            data = response_data.get("data", [])
            previous_number_of_users = num_of_records
            num_of_records += len(data)
            total_pages = response_data.get("total", 0)
            current_page = response_data.get("page", 0)
            for item in data:
                yield item

            if (
                current_page >= total_pages
                or previous_number_of_users == num_of_records
            ):
                break

            if params is None:
                params = {"page": current_page + 1}
            else:
                params = {**params, "page": current_page + 1}

            page_count += 1
            if page_limit is not None and page_count >= page_limit:
                break

        return all_data

    def get_users(
        self, page_size: int = 10, page_limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Retrieve a list of users from the API.

        Args:
            page_size (int, optional): Number of users to retrieve per page

        Returns:
            list: List of user objects.
        """
        url = f"{self.home_url}/user"
        params = {"limit": page_size}

        return self._paginate(url, params, page_limit)

    def get_posts_with_comments(
        self, page_size: int = 10, page_limit: int = 5
    ) -> List[Dict[str, Any]]:
        """
        Retrieve a list of posts with comments from the API.

        Args:
            page_size (int, optional): Number of posts to retrieve per page.
            Defaults to 50.

        Returns:
            list: List of post objects with comments.
        """
        url = f"{self.home_url}/post"
        params = {"limit": page_size}

        all_posts = self._paginate(url, params, page_limit)

        for post in all_posts:
            comments_url = f"{url}/{post['id']}/comment"
            post["comments"] = self._paginate(comments_url, params)

        return all_posts
