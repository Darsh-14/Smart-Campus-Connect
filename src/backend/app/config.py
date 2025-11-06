from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    SUPABASE_URL: str = "http://demo.local"
    SUPABASE_KEY: str = "demo_key"
    SUPABASE_SERVICE_KEY: str = "demo_service_key"
    JWT_SECRET_KEY: str = "demo_jwt_secret_key_for_development_only_12345"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"


settings = Settings()
