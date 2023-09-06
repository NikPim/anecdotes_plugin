# -*- coding: utf-8 -*-
class BaseError(ValueError):
    """
    Basic error class can be used to add some basic
    common functionality to more specific errors
    """

    def __init__(self, message: str = "Default error message") -> None:
        super().__init__(message)


class InvalidTokenError(BaseError):
    """
    Error raised when an invalid token is provided.
    """

    def __init__(self, message: str = "Invalid token provided") -> None:
        super().__init__(message)


class MissingTokenError(BaseError):
    """
    Error raised when no token is provided.
    """

    def __init__(self, message: str = "No token provided") -> None:
        super().__init__(message)


class ServerDoesNotRespondError(BaseError):
    """
    Error raised when a server does not respond.
    """

    def __init__(self, message: str = "Server does not respond") -> None:
        super().__init__(message)


class UnknownApiProviderError(BaseError):
    """
    Error raised when unable to create an API client instance
    """

    def __init__(
        self, message: str = "Unable to create an API client instance"
    ) -> None:
        super().__init__(message)


class APIConnectionError(Exception):
    """
    Error raised when there is a failure in the API connection.
    """

    def __init__(self, message: str = "Failed to connect to the API") -> None:
        super().__init__(message)
