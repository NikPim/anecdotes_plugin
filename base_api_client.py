from abc import ABC, abstractmethod
import error_classes as error
from read_config import read_config


class BaseAPIClient(ABC):
    """
    Client for interacting with the API provided by dummyapi.io service.
    """
    def __init__(self, url, auth_header):
        self.home_url = url
        self.header = auth_header

        # Check connectivity during class construction
        self.check_connection()

    @abstractmethod
    def check_connection(self):
        """
        Abstract method meant for checking connection
        """

    @abstractmethod
    def _paginate(self):
        """
        Paginate through the API responses to retrieve all data.
        """

    @abstractmethod
    def get_users(self):
        """
        Retrieve a list of users from the API.
        """

    @abstractmethod
    def get_posts_with_comments(self):
        """
        Retrieve a list of posts with comments from the API.
        """

    @staticmethod
    def create_instance(api_provider):
        """
        Creates an istance of a child class depending on a certain API we want to connect

        Args:
            api_provider (string): API provider name to fetch its credentials from a proper storage

        Returns:
            client (APIClient type): an instance of a specific APIClient type with input credentials
        """
        # Read the config file to get credentials to the exact API service
        config = read_config()

        url = config.get(api_provider, "base_url")
        header_name = config.get(api_provider, "header_name")
        token = config.get(api_provider, "token")


        if api_provider == "Dummy":
            from dummy_api_client import DummyAPIClient
            header = {header_name : token}
            client = DummyAPIClient(url, header)
        elif api_provider == "Any other API provider":
            pass
        else:
            raise error.WrongInstanceError()

        return client
