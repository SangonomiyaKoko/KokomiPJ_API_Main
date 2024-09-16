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
    
    class Config:
        env_file = ".env"

settings = Settings()
