"""Proxy routes for The Odds API (NBA)."""

from collections.abc import Generator

from fastapi import APIRouter, Depends, HTTPException
from fastapi.responses import JSONResponse

from nba_api import OddsApiClient
from nba_api.exceptions import OddsApiError
from nba_alpha_gen.config import get_settings

router = APIRouter(prefix="/api/v1/odds", tags=["odds"])


def get_odds_client() -> Generator[OddsApiClient]:
    settings = get_settings()
    if not settings.odds_api_key:
        raise HTTPException(
            status_code=503,
            detail="Odds API is not configured. Set environment variable NBA_ODDS_API_KEY.",
        )
    client = OddsApiClient(settings.odds_api_key, settings.odds_api_base_url)
    try:
        yield client
    finally:
        client.close()


def _odds_http_exception(exc: OddsApiError) -> HTTPException:
    if exc.status_code == 404:
        return HTTPException(status_code=404, detail=exc.args[0])
    if exc.status_code and 400 <= exc.status_code < 500:
        return HTTPException(status_code=exc.status_code, detail=exc.args[0])
    return HTTPException(status_code=502, detail=exc.args[0])


@router.get("/nba")
def get_nba_slate_odds(
    regions: str | None = None,
    markets: str | None = None,
    oddsFormat: str = "american",
    client: OddsApiClient = Depends(get_odds_client),
) -> JSONResponse:
    """Upcoming NBA games with bookmaker odds (h2h, spreads, totals by default)."""
    settings = get_settings()
    r = regions or settings.odds_default_regions
    m = markets or settings.odds_default_markets
    try:
        data, headers = client.get_nba_odds(regions=r, markets=m, odds_format=oddsFormat)
    except OddsApiError as e:
        raise _odds_http_exception(e) from e
    return JSONResponse(content=data, headers=headers)


@router.get("/nba/events/{event_id}")
def get_nba_event_odds(
    event_id: str,
    regions: str | None = None,
    markets: str | None = None,
    oddsFormat: str = "american",
    client: OddsApiClient = Depends(get_odds_client),
) -> JSONResponse:
    """Single-event odds (use for player props and additional markets)."""
    settings = get_settings()
    r = regions or settings.odds_default_regions
    m = markets or settings.odds_default_event_markets
    try:
        data, headers = client.get_nba_event_odds(
            event_id,
            regions=r,
            markets=m,
            odds_format=oddsFormat,
        )
    except OddsApiError as e:
        raise _odds_http_exception(e) from e
    return JSONResponse(content=data, headers=headers)
