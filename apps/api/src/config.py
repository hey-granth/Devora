
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    # Database
    database_url: str

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Security
    secret_key: str
    api_key_hash_salt: str

    # AI/LLM
    litellm_default_model: str = "gpt-4o-mini"
    openai_api_key: str | None = None
    anthropic_api_key: str | None = None
    embedding_model: str = "text-embedding-3-small"

    # Environment
    environment: str = "development"
    cors_origins: list[str] = ["http://localhost:3000"]

    class Config:
        env_file = ".env"


settings = Settings()
