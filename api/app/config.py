from pydantic import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    API_KEY: str
    LIVY_SERVER: str
    class Config:
        env_file = "app/.env"

# New decorator for cache
@lru_cache()
def get_settings():
    return Settings()