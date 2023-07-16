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

    def _paginate(self, url, params=None, page_limit = None):
        """
        Paginate through the API responses to retrieve all data.

        Args:
            url (str): The base URL for the API endpoint.
            params (dict, optional): Additional query parameters. Defaults to None.

        Returns:
            list: List of data objects retrieved from paginated API responses.
        """
        all_data = []
        page_count = 0

        while True:
            response = requests.get(url, headers=self.headers, params=params, timeout=5)
            response_data = response.json()

            data = response_data.get("data", [])
            previous_number_of_users = len(all_data)
            all_data.extend(data)

            total_pages = response_data.get("total", 0)
            current_page = response_data.get("page", 0)

            if current_page >= total_pages or previous_number_of_users == len(all_data):
                break

            if params is None:
                params = {"page": current_page + 1}
            else:
                params = {**params, "page": current_page + 1}

            page_count += 1
            if page_limit is not None and page_count >= page_limit:
                break

        return all_data

    def get_users(self, page_size=10, page_limit=None):
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

    def get_posts_with_comments(self, page_size=10, page_limit=None):
        """
        Retrieve a list of posts with comments from the API.

        Args:
            page_size (int, optional): Number of posts to retrieve per page. Defaults to 50.

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
