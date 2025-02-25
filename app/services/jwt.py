from jose import jwt, ExpiredSignatureError, JWTError

from datetime import datetime, timedelta

from config import settings

from schemas.user import UserRole
from schemas.jwt import TokenData, TokenResponse

from exceptions.jwt import TokenInvalid

class TokenService:

    ACCESS_SECRET_KEY = settings.ACCESS_SECRET_KEY
    REFRESH_SECRET_KEY = settings.REFRESH_SECRET_KEY
    ALGORITHM = settings.ALGORITHM
    ACCESS_TOKEN_EXPIRE_MINUTES = 15
    REFRESH_TOKEN_EXPIRE_DAYS = 7

    def create_access_token(self, username: str, role: UserRole) -> str:
        token_data = {
            "username": username,
            "role": role
        }
        token_data["expire"] = datetime.now() + timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        token_data["expire"] = token_data["expire"].isoformat()
        return jwt.encode(token_data, self.ACCESS_SECRET_KEY, algorithm=self.ALGORITHM)
    
    def create_refresh_token(self, username: str, role: UserRole):
        token_data = {
            "username": username,
            "role": role
        }
        token_data["expire"] = datetime.now() + timedelta(days=self.REFRESH_TOKEN_EXPIRE_DAYS)
        token_data["expire"] = token_data["expire"].isoformat()
        return jwt.encode(token_data, self.REFRESH_SECRET_KEY, algorithm=self.ALGORITHM)
    
    def decode_token(self, token: str, is_refresh: bool = False) -> TokenData:
        secret: str
        if is_refresh:
            secret = self.REFRESH_SECRET_KEY
        else:
            secret = self.ACCESS_SECRET_KEY
        try:
            payload = TokenData(**jwt.decode(token, secret, algorithms=[self.ALGORITHM]))
            if payload.role not in UserRole.__members__:
                raise TokenInvalid
            if payload.username is None:
                raise TokenInvalid
            return payload
        except JWTError:
            raise TokenInvalid
    
    def refresh_tokens(self, refresh_token: str) -> TokenResponse:
        payload = self.decode_token(refresh_token, True)
        new_access_token = self.create_access_token(payload.username, payload.role)
        new_refresh_token = self.create_refresh_token(payload.username, payload.role)
        return TokenResponse(access_token=new_access_token, refresh_token=new_refresh_token)
    
token_service = TokenService()