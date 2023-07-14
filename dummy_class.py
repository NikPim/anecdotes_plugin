import requests

class InvalidTokenError(ValueError):
    """
    Error raised when an invalid token is provided.
    """
    def __init__(self, message="Invalid token provided"):
        super().__init__(message)

class MissingTokenError(ValueError):
    """
    Error raised when no token is provided.
    """
    def __init__(self, message="No token provided"):
        super().__init__(message)

class ServerDoesNotRespondError(ValueError):
    """
    Error raised when a server does not respond.
    """
    def __init__(self, message="Server does not respond"):
        super().__init__(message)

class APIConnectionError(Exception):
    """
    Error raised when there is a failure in the API connection.
    """
    def __init__(self, message="Failed to connect to the API"):
        super().__init__(message)


class DummyAPIClient:
    """
    Client for interacting with the API provided by dummyapi.io service.
    """
    def __init__(self, url, access_token):
        self.home_url = url
        self.headers = {"app-id": access_token}

        # Check connectivity during class construction
        self.check_connection()

    def check_connection(self):
        """
        Check the connection to the API.

        Raises:
            ValueError: If an invalid token is provided.
            ValueError: If no token is provided.
            Exception: If there is a failure to connect to the API.
        """
        url = f"{self.home_url}/user"
        response = requests.get(url, headers=self.headers, timeout=5)
        if response.status_code == 200:
            return

        if response.status_code == 403:
            error_data = response.json().get("error", {})
            if error_data == "APP_ID_NOT_EXIST":
                raise InvalidTokenError()
            if error_data == "APP_ID_MISSING":
                raise MissingTokenError()

        if response.status_code == 404:
            raise ServerDoesNotRespondError()

        raise APIConnectionError()

    def _paginate(self, url, params=None):
        """
        Paginate through the API responses to retrieve all data.

        Args:
            url (str): The base URL for the API endpoint.
            params (dict, optional): Additional query parameters. Defaults to None.

        Returns:
            list: List of data objects retrieved from paginated API responses.
        """
        all_data = []

        while url:
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            data = response.json().get("data", [])
            all_data.extend(data)

            pagination = response.json().get("pagination", {})
            url = pagination.get("next", None)
            params = None  # Clear the params after the first request

        return all_data

    def get_users(self, page_size=5, total_pages=2):
        """
        Retrieve a list of users from the API.

        Args:
            page_size (int, optional): Number of users to retrieve per page. Defaults to 50.
            total_pages (int, optional): Maximum number of pages to retrieve. Defaults to 10.

        Returns:
            list: List of user objects.
        """
        url = f"{self.home_url}/user"
        params = {"limit": page_size}

        return self._paginate(url, params)

    def get_posts_with_comments(self, page_size=5, total_pages=2):
        """
        Retrieve a list of posts with comments from the API.

        Args:
            page_size (int, optional): Number of posts to retrieve per page. Defaults to 50.
            total_pages (int, optional): Maximum number of pages to retrieve. Defaults to 1.

        Returns:
            list: List of post objects with comments.
        """
        url = f"{self.home_url}/post"
        params = {"limit": page_size}

        all_posts = self._paginate(url, params)

        for post in all_posts:
            comments_url = f"{url}/{post['id']}/comment"
            post["comments"] = self._paginate(comments_url)

        return all_posts
