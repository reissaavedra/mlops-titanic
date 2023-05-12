import os

from pydantic import BaseSettings


class Settings(BaseSettings):
    DB_USER: str = os.getenv("DB_USER", "titanic")
    DB_PASSWORD: str = os.getenv("DB_PASSWORD", "titanic")
    DB_HOST: str = os.getenv("DB_HOST", "localhost")
    DB_NAME: str = os.getenv("DB_NAME", "titanic")

    class Config:
        case_sensitive = True


settings = Settings()
