# app/core/config.py

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "FactoryControl API"
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        extra = "allow"

settings = Settings()
