from exceptions.base import BaseAPIException

from fastapi import status

class TokenInvalid(BaseAPIException):
    message = "Invalid token"
    status_code = status.HTTP_401_UNAUTHORIZED

class RefreshTokenMissing(BaseAPIException):
    message = "Refresh token missing!"
    status_code = status.HTTP_401_UNAUTHORIZED