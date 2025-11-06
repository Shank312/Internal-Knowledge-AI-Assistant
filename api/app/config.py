

from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_env: str = Field("dev", alias="APP_ENV")
    openai_api_key: str | None = Field(default=None, alias="REDACTED")

    pg_user: str = Field("brain", alias="POSTGRES_USER")
    pg_pass: str = Field("brainpass", alias="POSTGRES_PASSWORD")
    pg_db: str = Field("company_brain", alias="POSTGRES_DB")
    pg_host: str = Field("localhost", alias="POSTGRES_HOST")
    pg_port: int = Field(5432, alias="POSTGRES_PORT")

    redis_url: str = Field("redis://localhost:6379/0", alias="REDIS_URL")

    minio_access_key: str = Field("minio", alias="MINIO_ROOT_USER")
    minio_secret_key: str = Field("minio123", alias="MINIO_ROOT_PASSWORD")
    minio_bucket: str = Field("company-brain", alias="MINIO_BUCKET")
    minio_endpoint_url: str = Field("http://localhost:9000", alias="MINIO_ENDPOINT_URL")
    minio_region: str = Field("us-east-1", alias="MINIO_REGION")

    default_tenant_id: str = Field("tenant_demo", alias="DEFAULT_TENANT_ID")

    embedding_model: str = Field("text-embedding-3-small", alias="EMBEDDING_MODEL")
    llm_model: str = Field("gpt-4o-mini", alias="LLM_MODEL")
    top_k: int = Field(6, alias="TOP_K")
    max_tokens: int = Field(500, alias="MAX_TOKENS")
    temperature: float = Field(0.2, alias="TEMPERATURE")

    class Config:
        extra = "ignore"
        env_file = ".env"

settings = Settings()
