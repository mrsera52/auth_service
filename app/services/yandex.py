from datetime import datetime

from config import settings

import requests
from requests.exceptions import RequestException, JSONDecodeError

from schemas.yandex import YandexAuthResponse, YandexInfoResponse

from exceptions.yandex import InternalError

class OAuthService:

    CLIENT_ID = settings.CLIENT_ID
    CLIENT_SECRET = settings.CLIENT_SECRET
    TOKEN_LINK = "https://oauth.yandex.ru/token"
    INFO_LINK = "https://login.yandex.ru/info"
    AUTH_LINK = f"ps://oauth.yandex.ru/authorize?response_type=code&client_id={CLIENT_ID}"

    def get_tokens(self, code: str):
        token_data = {
            "grant_type": "authorization_code",
            "code": code,
            "client_id": self.CLIENT_ID,
            "client_secret": self.CLIENT_SECRET
        }
        try:
            response = requests.post("https://oauth.yandex.ru/token", data=token_data)
            data = response.json()
            return YandexAuthResponse.model_validate(data)
        except RequestException:
            raise InternalError
        except JSONDecodeError:
            raise InternalError

    def get_user_info(self, access_token: str):
        headers = {
            "Authorization": f"OAuth {access_token}"
        }
        response = requests.get(self.INFO_LINK, headers=headers)
        data = response.json()
        return YandexInfoResponse(username=data["login"])

    def is_access_token_expired(expiry: datetime):
        pass



oauth_service = OAuthService()