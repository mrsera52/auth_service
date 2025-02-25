from exceptions.base import BaseAPIException

from fastapi import status

class InternalError(BaseAPIException):
    message = "Internal Server Error."
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR