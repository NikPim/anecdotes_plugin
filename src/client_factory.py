# -*- coding: utf-8 -*-
import error_classes as error
from read_config import read_config
from base_api_client import BaseAPIClient


class APIClientFactory:
    @staticmethod
    def create_client(api_provider: str) -> BaseAPIClient:
        config = read_config()

        url = config.get(api_provider, "base_url")
        header_name = config.get(api_provider, "header_name")
        token = config.get(api_provider, "token")

        if api_provider == "Dummy":
            from dummy_api_client import DummyAPIClient

            header = {header_name: token}
            return DummyAPIClient(url, header)

        raise error.UnknownApiProviderError()
