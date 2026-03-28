"""Tests for OddsApiClient (mocked HTTP)."""

import httpx
import pytest
from fastapi.testclient import TestClient

from nba_api import OddsApiClient
from nba_api.constants import SPORT_KEY
from nba_api.exceptions import OddsApiError
from nba_alpha_gen.main import create_app


def test_get_nba_odds_requests_correct_path_and_params() -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["url"] = str(request.url)
        return httpx.Response(200, json=[])

    transport = httpx.MockTransport(handler)
    with OddsApiClient("secret-key", transport=transport) as client:
        data, headers = client.get_nba_odds(regions="us", markets="h2h,spreads,totals")

    assert data == []
    assert "apiKey=secret-key" in captured["url"]
    assert f"/sports/{SPORT_KEY}/odds" in captured["url"]
    assert "regions=us" in captured["url"]
    assert "markets=h2h%2Cspreads%2Ctotals" in captured["url"] or "markets=h2h,spreads,totals" in captured["url"]


def test_get_nba_event_odds_requests_event_path() -> None:
    captured: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["path"] = request.url.path
        return httpx.Response(200, json={"id": "evt1"})

    transport = httpx.MockTransport(handler)
    with OddsApiClient("k", transport=transport) as client:
        data, _ = client.get_nba_event_odds(
            "abc123",
            regions="us",
            markets="player_points",
        )

    assert data == {"id": "evt1"}
    assert captured["path"].endswith(f"/sports/{SPORT_KEY}/events/abc123/odds")


def test_raises_odds_api_error_on_http_401() -> None:
    def handler(request: httpx.Request) -> httpx.Response:
        return httpx.Response(401, text="invalid key")

    transport = httpx.MockTransport(handler)
    with OddsApiClient("bad", transport=transport) as client:
        with pytest.raises(OddsApiError) as ei:
            client.get_nba_odds(regions="us", markets="h2h")
    assert ei.value.status_code == 401


def test_odds_routes_return_503_without_api_key(monkeypatch: pytest.MonkeyPatch) -> None:
    from nba_alpha_gen.config import Settings

    def fake_settings() -> Settings:
        return Settings(odds_api_key=None)

    monkeypatch.setattr("nba_alpha_gen.routers.odds.get_settings", fake_settings)
    client = TestClient(create_app())
    r = client.get("/api/v1/odds/nba")
    assert r.status_code == 503


def test_odds_routes_proxy_with_mocked_upstream(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("NBA_ODDS_API_KEY", "test-key")

    def handler(request: httpx.Request) -> httpx.Response:
        if "/events/" in request.url.path:
            return httpx.Response(200, json={"id": "e1", "bookmakers": []})
        return httpx.Response(200, json=[{"id": "g1"}])

    transport = httpx.MockTransport(handler)

    import nba_alpha_gen.routers.odds as odds_router_mod

    real_client = OddsApiClient

    def patched_client(*args: object, **kwargs: object) -> OddsApiClient:
        kwargs = dict(kwargs)
        kwargs["transport"] = transport
        return real_client(*args, **kwargs)

    monkeypatch.setattr(odds_router_mod, "OddsApiClient", patched_client)

    client = TestClient(create_app())
    r = client.get("/api/v1/odds/nba")
    assert r.status_code == 200
    assert r.json() == [{"id": "g1"}]

    r2 = client.get("/api/v1/odds/nba/events/e1")
    assert r2.status_code == 200
    assert r2.json()["id"] == "e1"


@pytest.mark.integration
@pytest.mark.skipif(
    not __import__("os").environ.get("NBA_ODDS_API_KEY"),
    reason="Set NBA_ODDS_API_KEY to run integration test against The Odds API",
)
def test_live_odds_api_smoke() -> None:
    """Single minimal request: slate + moneyline only (lowest credit use for a smoke test)."""
    import os

    key = os.environ["NBA_ODDS_API_KEY"]
    with OddsApiClient(key) as c:
        data, _ = c.get_nba_odds(regions="us", markets="h2h")
    assert isinstance(data, list)
