from schemas.user import RegisterSchema, LoginSchema, UserRole, UserToCreate, UserResponse

from exceptions.user import UserAlreadyExists

from config import settings

from passlib.context import CryptContext

class UserService:

    ALGORITHM = settings.HASH_ALGORITHM

    def __init__(self):
        self.password_context = CryptContext(schemes=[self.ALGORITHM])

    def hash_password(self, password: str) -> str:
        return self.password_context.hash(password)
    
    def verify_password(self, entered_password: str, hashed_password: str) -> bool:
        return self.password_context.verify(entered_password, hashed_password)
    
    async def check_exists_user(self, username: str) -> bool:
        False

    async def create_user(self, user: UserToCreate) -> UserResponse:
        if self.check_exists_user(user.username):
            raise UserAlreadyExists
        
        return UserResponse(username=user.username, email=user.email)

    async def get_user(self, data: LoginSchema):
        pass

user_service = UserService()