from pydantic import BaseModel

from datetime import datetime

from schemas.user import UserRole

class TokenData(BaseModel):
    expire: datetime
    username: str
    role: UserRole

class TokenResponse(BaseModel):
    access_token: str
    refresh_token: str
