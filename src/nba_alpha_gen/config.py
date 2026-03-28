from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict

from nba_api.constants import DEFAULT_BASE_URL


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="NBA_", env_file=".env", extra="ignore")

    app_name: str = "NBA Alpha Gen"
    debug: bool = False
    cors_origins: str = (
        "http://localhost:3000,http://127.0.0.1:3000,"
        "http://localhost:5173,http://127.0.0.1:5173"
    )

    odds_api_key: str | None = Field(
        default=None,
        description="The Odds API key (https://the-odds-api.com/). Env: NBA_ODDS_API_KEY",
    )
    odds_api_base_url: str = Field(
        default=DEFAULT_BASE_URL,
        description="The Odds API v4 base URL. Env: NBA_ODDS_API_BASE_URL",
    )
    odds_default_regions: str = Field(
        default="us",
        description="Default regions for Odds API (e.g. us). Env: NBA_ODDS_DEFAULT_REGIONS",
    )
    odds_default_markets: str = Field(
        default="h2h,spreads,totals",
        description="Default markets for slate odds. Env: NBA_ODDS_DEFAULT_MARKETS",
    )
    odds_default_event_markets: str = Field(
        default="player_points,player_rebounds,player_assists,player_threes",
        description="Default markets for per-event odds (props). Env: NBA_ODDS_DEFAULT_EVENT_MARKETS",
    )


def get_settings() -> Settings:
    return Settings()
