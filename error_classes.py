class BaseError(ValueError):
    """
    Basic error class can be used to add some basic common functionality to more specific errors
    """
    def __init__(self, message="Default error message"):
        super().__init__(message)

class InvalidTokenError(BaseError):
    """
    Error raised when an invalid token is provided.
    """
    def __init__(self, message="Invalid token provided"):
        super().__init__(message)

class MissingTokenError(BaseError):
    """
    Error raised when no token is provided.
    """
    def __init__(self, message="No token provided"):
        super().__init__(message)

class ServerDoesNotRespondError(BaseError):
    """
    Error raised when a server does not respond.
    """
    def __init__(self, message="Server does not respond"):
        super().__init__(message)

class WrongInstanceError(BaseError):
    """
    Error raised when unable to create an API client instance
    """
    def __init__(self, message="Unable to create an API client instance"):
        super().__init__(message)

class APIConnectionError(Exception):
    """
    Error raised when there is a failure in the API connection.
    """
    def __init__(self, message="Failed to connect to the API"):
        super().__init__(message)
