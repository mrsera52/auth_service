from pydantic import BaseModel, EmailStr

from enum import Enum

class UserRole(str, Enum):
    regular = "regular"
    admin = "admin"

class RegisterSchema(BaseModel):
    email: EmailStr
    username: str
    password: str

class LoginSchema(BaseModel):
    username: str
    password: str

class UserToCreate(RegisterSchema):
    role: UserRole

class UserResponse(BaseModel):
    username: str
    email: EmailStr

class AuthType(str, Enum):
    local = "local"
    yandex = "yandex"