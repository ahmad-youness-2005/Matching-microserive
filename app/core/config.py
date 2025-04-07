import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "Dating App API"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./test.db")
    
    BACKEND_CORS_ORIGINS: list = ["*"]
    
    API_TITLE: str = "Dating App API"
    API_DESCRIPTION: str = "API for dating app preferences and matching"
    API_VERSION: str = "1.0.0"
    
    class Config:
        env_file = ".env"

settings = Settings() 