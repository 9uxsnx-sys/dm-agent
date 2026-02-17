from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://user:password@db/ai_sales_agent"
    REDIS_URL: str = "redis://redis:6379/0"
    HF_API_KEY: str = ""
    N8N_HOST: str = "localhost"
    N8N_PORT: int = 5678
    WEBHOOK_SECRET: str = ""
    ENVIRONMENT: str = "development"
    USE_MOCK_REDIS: bool = False

    class Config:
        env_file = ".env"

settings = Settings()
REDIS_URL = settings.REDIS_URL
WEBHOOK_SECRET = settings.WEBHOOK_SECRET
