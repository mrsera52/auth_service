from typing import Optional
from pydantic_settings import BaseSettings
import pydantic
import urllib

class Settings(BaseSettings):
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int

    ACCESS_SECRET_KEY: str
    ALGORITHM: str
    REFRESH_SECRET_KEY: str

    CLIENT_ID: str
    CLIENT_SECRET: str

    HASH_ALGORITHM: str

    DB_URL: Optional[pydantic.AnyUrl] = None

    RABBITMQ_USER: str
    RABBITMQ_PASSWORD: str

    @pydantic.model_validator(mode="after")
    def build_db_link(cls, values: "Settings"):
        if not values.DB_URL:
            values.DB_URL = pydantic.PostgresDsn.build(
                scheme="postgresql+asyncpg",
                username=values.POSTGRES_USER,     
                password=values.POSTGRES_PASSWORD,
                host=values.POSTGRES_HOST,
                port=values.POSTGRES_PORT,
                path=values.POSTGRES_DB,  
            )
        return values


settings = Settings()
