from exceptions.base import BaseAPIException

from fastapi import status

class UserAlreadyExists(BaseAPIException):
    message = "User already exists. Please try another username."
    status_code = status.HTTP_409_CONFLICT