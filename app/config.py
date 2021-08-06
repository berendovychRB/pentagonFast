import os
from functools import lru_cache

from pydantic import BaseSettings

ROOT_DIR = os.path.abspath(os.curdir)
SECRET_PATH = os.path.join(ROOT_DIR, 'config/local/')


class Settings(BaseSettings):
    SECRET_KEY: str
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    POSTGRES_DATABASE_URL: str = "postgresql://username:password@db:5432/api"

    class Config:
        env_file = os.path.join(SECRET_PATH, "secrets.env")


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()
