# -*- coding: utf-8 -*-

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_HOST: str
    API_PORT: int

    MYSQL_HOST: str
    MYSQL_PORT: int
    MYSQL_USERNAME: str
    MYSQL_PASSWORD: str
    
    REDIS_HOST: str
    REDIS_PORT: int
    REDIS_PASSWORD: str

    SQLITE_PATH: str
    
    WG_API_TOKEN: str
    LESTA_API_TOKEN: str
    CN_API_TOKEN: str
    CALL_API_TIMEOUT: int

    CLAN_CACHE_VALIDITY: int
    CLAN_CACHE_VALIDITY_2: int

    class Config:
        env_file = ".env"

settings = Settings()
