"""
/core/exceptions.py

This module defines the base exception for the APIs. Features subclass
APIException to declare their own errors, and the handler registered in
main.py turns any of them into a ResponseModel JSON response.
"""

# Importing the necessary modules
from typing import Any

class APIException(Exception):
    """
    Base exception for all API errors in the application.

    Subclasses set their own api_status_code and api_status_message as class
    attributes. Because the handler is registered for APIException, it also
    handles every subclass.

    Attributes:
        api_status_code (int): The status code of the API response. Its
            leading three digits are the HTTP status code (e.g. 40401 -> 404).
            Defaults to 50000.
        api_status_message (str): The error message of the API response.
            Defaults to "Internal server error".
        data (Any): Optional extra details about the error, returned in the
            response's data field.

    Example:
        class UserNotFound(APIException):
            api_status_code = 40401
            api_status_message = "User not found"

        raise UserNotFound(data={"user_id": 7})
    """

    # Defaults used when a subclass doesn't set its own code / message.
    api_status_code: int = 50000
    api_status_message: str = "Internal server error"

    def __init__(self, message: str | None = None, data: Any = None):
        """
        Initializes the exception.

        Args:
            message (str | None): The error message. If not given, the class's
                api_status_message is used.
            data (Any): Optional extra details about the error. Defaults to None.
        """
        self.api_status_message = message or self.api_status_message
        self.data = data
        super().__init__(self.api_status_message)

    @property
    def server_status_code(self) -> int:
        """
        Returns the HTTP status code of the response.

        Returns:
            int: The api_status_code without its last two digits
                (e.g. 40401 -> 404).
        """
        return self.api_status_code // 100