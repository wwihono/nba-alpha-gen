from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NBA_", env_file=".env", extra="ignore")

    app_name: str = "NBA Alpha Gen"
    debug: bool = False
    cors_origins: str = "http://localhost:3000,http://127.0.0.1:3000"


def get_settings() -> Settings:
    return Settings()
