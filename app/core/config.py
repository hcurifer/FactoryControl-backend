# app/core/config.py

from pydantic_settings import BaseSettings
from pydantic import Field, model_validator

class Settings(BaseSettings):
    PROJECT_NAME: str = "FactoryControl API"
    API_V1_PREFIX: str = "/api/v1"
    
    # Variables del archivo .env
    
    # DB
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 0
    DB_NAME: str = ""
    
    # JWT / AUTH
    JWT_SECRET_KEY: str = Field(default="")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_HOURS: int = 10


    class Config:
        env_file = ".env"
        extra = "allow"
        
    @property
    def DATABASE_URL(self):
        
        return (
            f"postgresql+psycopg2://{self.DB_USER}:{self.DB_PASSWORD}"
            f"@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
        
    @model_validator(mode="after")
    def validate_auth_config(self):
        if not self.JWT_SECRET_KEY:
            raise ValueError("JWT_SECRET_KEY no está definido en el .env")
        return self

    # EMAIL / SMTP (Gmail)
    EMAIL_ENABLED: bool = False
    EMAIL_DEFAULT_TO: str = ""

    SMTP_HOST: str = "smtp.gmail.com"
    SMTP_PORT: int = 587
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""
    SMTP_FROM: str = ""

settings = Settings()
