from typing import Any
from fastapi import status


class AppException(Exception):
    def __init__(self, message: str, status_code: int = 500, data: Any = None):
        self.message = message
        self.status_code = status_code
        self.data = data

        super().__init__(message)


class UnauthorizedException(AppException):
    def __init__(self, message: str = "Unauthorized"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)


class InvalidRefreshTokenError(AppException):
    def __init__(self, message: str = "Invalid token"):
        super().__init__(message, status_code=status.HTTP_401_UNAUTHORIZED)
