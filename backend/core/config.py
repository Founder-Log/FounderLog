from urllib.parse import quote_plus

from pydantic import model_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "FounderLog"
    debug: bool = True

    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "founderlog"
    postgres_host: str = "127.0.0.1"
    postgres_port: int = 5433

    database_url: str = ""

    jwt_secret: str = "change-me"
    jwt_algorithm: str = "HS256"
    access_token_expire_minutes: int = 30

    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore",
    )

    @model_validator(mode="after")
    def _build_database_url(self):
        if not self.database_url:
            self.database_url = (
                f"postgresql+asyncpg://{quote_plus(self.postgres_user)}:"
                f"{quote_plus(self.postgres_password)}@"
                f"{self.postgres_host}:{self.postgres_port}/{self.postgres_db}"
            )
        return self


settings = Settings()