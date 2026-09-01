from functools import lru_cache
from pathlib import Path

from pydantic import BaseModel, Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

BASE_DIR = Path(__file__).resolve().parents[3]


class Jwt(BaseModel):
    secret_key: str = Field(
        ...,
        description="JWT secret key",
    )
    algorithm: str = Field(
        default="HS256",
        description="JWT algorithm",
    )
    access_token_expire_minutes: int = Field(
        default=30,
        description="Access token expiration time in minnutes",
    )

class Api(BaseModel):
    prefix: str = Field(
        default="/api",
        description="API base path",
    )


class App(BaseModel):
    title: str = Field(
        default="FastAPI",
        description="Application title",
    )
    environment: str = Field(
        default="dev",
        description="Application environment",
    )
    debug: bool = Field(
        default=False,
        description="Application debug mode",
    )

    @field_validator("environment")
    @classmethod
    def validate_environment(cls, v: str) -> str:
        if v not in ("dev", "prod", "test", "staging"):
            raise ValueError(
                f"Invalid environment: {v}. Must be 'dev', 'prod', ''test' or 'staging'"
            )
        return v


class Database(BaseModel):
    url_async: str = Field(
        ...,
        description="Database connection string",
    )
    echo: bool = Field(
        default=False,
        description="Database echo mode",
    )

    @field_validator("url_async")
    @classmethod
    def validate_url_async(cls, v: str) -> str:
        """Validate that url_async is a valid database URL."""

        if not v.startswith(
            ("postgresql+asyncpg://", "postgresql://", "sqlite+aiosqlite://")
        ):
            raise ValueError(
                f"Invalid database URL format for DATABASE__URL_ASYNC: '{v}'. "
                "Expected format: postgresql+asyncpg://user:password@host:port/dbname"
            )
        return v


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=str(BASE_DIR / ".env"),
        env_file_encoding="utf-8",
        extra="ignore",
        env_nested_delimiter="__",
    )

    app: App
    api: Api
    database: Database
    jwt: Jwt


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    return Settings()  # type: ignore
