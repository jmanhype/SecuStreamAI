from pydantic_settings import BaseSettings
from pydantic import Field
from pathlib import Path
from typing import Optional
import os

class Settings(BaseSettings):
    # Project Information
    PROJECT_NAME: str = Field("Security Event Processor", env="PROJECT_NAME")
    PROJECT_VERSION: str = Field("1.0.0", env="PROJECT_VERSION")
    API_V1_STR: str = Field("/api/v1", env="API_V1_STR")
    
    # Kafka Configuration
    KAFKA_SERVER: str = Field("localhost:29092", env="KAFKA_SERVER")
    KAFKA_TOPIC: str = Field("security-events", env="KAFKA_TOPIC")
    
    # Redis Configuration
    REDIS_HOST: str = Field("localhost", env="REDIS_HOST")
    REDIS_PORT: int = Field(6379, env="REDIS_PORT")
    
    # Prometheus Configuration
    PROMETHEUS_PORT: int = Field(8000, env="PROMETHEUS_PORT")
    
    # OpenAI Configuration
    OPENAI_API_KEY: str = Field(..., env="OPENAI_API_KEY")  # Required environment variable
    
    # Security Configuration
    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field("HS256", env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    
    # PostgreSQL Configuration
    POSTGRES_HOST: str = Field("localhost", env="POSTGRES_HOST")
    POSTGRES_PORT: str = Field("5432", env="POSTGRES_PORT")
    POSTGRES_DB: str = Field("secustreamai", env="POSTGRES_DB")
    POSTGRES_USER: str = Field("secustreamai_user", env="POSTGRES_USER")
    POSTGRES_PASSWORD: str = Field(..., env="POSTGRES_PASSWORD")

    # Celery Configuration
    CELERY_BROKER_URL: str = Field(os.getenv('CELERY_BROKER_URL', 'redis://redis:6379/0'), env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(os.getenv('CELERY_RESULT_BACKEND', 'redis://redis:6379/0'), env="CELERY_RESULT_BACKEND")

    @property
    def SQLALCHEMY_DATABASE_URL(self):
        """
        Constructs the SQLAlchemy Database URL using the loaded environment variables.
        """
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@" \
               f"{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        # Specify the absolute path to the .env file located at the project root
        env_file = Path(__file__).resolve().parent.parent.parent / ".env"
        env_file_encoding = 'utf-8'

settings = Settings()

# Debug prints to confirm .env path and loaded variables
print(f"Loading .env from: {settings.Config.env_file}")
print(f"OPENAI_API_KEY: {'Loaded' if settings.OPENAI_API_KEY else 'Not Loaded'}")
print(f"SECRET_KEY: {'Loaded' if settings.SECRET_KEY else 'Not Loaded'}")
print(f"POSTGRES_PASSWORD: {'Loaded' if settings.POSTGRES_PASSWORD else 'Not Loaded'}")
print(f"CELERY_BROKER_URL: {settings.CELERY_BROKER_URL}")
print(f"CELERY_RESULT_BACKEND: {settings.CELERY_RESULT_BACKEND}")