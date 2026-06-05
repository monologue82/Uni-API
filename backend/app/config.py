import os

from pydantic_settings import BaseSettings

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class Settings(BaseSettings):
    app_name: str = "Uni-API"
    app_version: str = "1.0.0"
    debug: bool = False

    database_url: str = f"sqlite+aiosqlite:///{os.path.join(BASE_DIR, 'data', 'uniapi.db')}"

    secret_key: str = "change-me-in-production-use-a-random-string"
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 1440

    route_cache_refresh_seconds: int = 30

    max_connections: int = 500
    max_keepalive_connections: int = 200
    keepalive_expiry: int = 30
    default_timeout: int = 30

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
