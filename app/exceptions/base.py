from fastapi import HTTPException, status

class BaseAPIException(HTTPException):

    message: str = "Something Went Wrong!"
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR

    def __init__(self):
        super().__init__(status_code=self.status_code, detail=self.message)
        