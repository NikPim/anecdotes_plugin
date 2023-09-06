# -*- coding: utf-8 -*-
import error_classes as error
from config.read_config import read_config
from base_api_client import BaseAPIClient


class APIClientFactory:
    """
    Factory class for creating API client instances based on the specified API provider.
    """

    @staticmethod
    def create_client(api_provider: str) -> BaseAPIClient:
        """
        Create and return an instance of the appropriate API client.

        Args:
            api_provider (str): The name of the API provider
            for which to create the client.

        Returns:
            BaseAPIClient: An instance of the API client
            corresponding to the given provider.

        Raises:
            error.UnknownApiProviderError: If the specified
            API provider is not recognized.
        """
        config = read_config()

        url = config.get(api_provider, "base_url")
        header_name = config.get(api_provider, "header_name")
        token = config.get(api_provider, "token")

        if api_provider == "Dummy":
            from dummy_api_client import DummyAPIClient

            header = {header_name: token}
            return DummyAPIClient(url, header)

        raise error.UnknownApiProviderError()
