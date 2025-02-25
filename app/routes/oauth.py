from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse

import requests

from services.yandex import oauth_service

router = APIRouter()

@router.get("/auth/login/yandex")
async def OAuth():
    return RedirectResponse(oauth_service.AUTH_LINK)

@router.post("/auth/callback/yandex")
async def auth_callback(request: Request):
    code = request.query_params.get("code")
    token_response = oauth_service.get_tokens(code)
    user_info = oauth_service.get_user_info(access_token=token_response.access_token)
    # если нет пользователя, создать. Если есть, авторизовать
    pass


@router.get("/auth/refresh/yandex")
async def refresh():
    pass