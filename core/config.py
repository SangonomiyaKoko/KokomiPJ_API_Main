# -*- coding: utf-8 -*-

from pydantic import BaseSettings

class Settings(BaseSettings):
    API_STR: str = "/api/v1"
    PROJECT_NAME: str = "FastAPI Multi-Version Project"
    SQLALCHEMY_DATABASE_URI: str = "mysql://user:password@localhost/dbname"
    
    class Config:
        env_file = ".env"

settings = Settings()
