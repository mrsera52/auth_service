from fastapi import APIRouter, Request, Response

from schemas.user import RegisterSchema, UserToCreate, UserRole, LoginSchema, AuthType
from schemas.jwt import TokenResponse

from services.user import user_service
from services.jwt import token_service
from services.rabbit import RabbitMQProducer

from exceptions.jwt import RefreshTokenMissing

from config import settings

router = APIRouter()

@router.post("/auth/register")
async def register(user: RegisterSchema):
    producer = RabbitMQProducer(rabbitmq_url=f"amqp://{settings.RABBITMQ_USER}:{settings.RABBITMQ_PASSWORD}@rabbitmq:5672/")
    await producer.publish_message(
        {"username": user.username},
        queue_name="registration"
    )
    await producer.close()
    return await user_service.create_user(UserToCreate(**user.model_dump(), role="regular"))
    

@router.post("/auth/login")
async def login(user: LoginSchema):
    # dao
    role = "regular"
    access_token = token_service.create_access_token(username=user.username, role=role)
    refresh_token = token_service.create_refresh_token(username=user.username, role=role)
    response = Response()
    response.set_cookie(key="access_token", value=access_token, httponly=True, samesite="strict")
    response.set_cookie(key="refresh_token", value=refresh_token, httponly=True, samesite="strict")
    response.set_cookie(key="auth_type", value=AuthType.local)
    return response

@router.post("/auth/refresh")
async def refresh(request: Request):
    refresh_token = request.cookies.get("refresh_token")
    if not refresh_token:
        raise RefreshTokenMissing
    tokens = token_service.refresh_tokens(refresh_token=refresh_token)
    response = Response()
    response.set_cookie(key="access_token", value=tokens.access_token, httponly=True, samesite="strict")
    response.set_cookie(key="refresh_token", value=tokens.refresh_token, httponly=True, samesite="strict")
    return response

