"""HTTP client for The Odds API v4 (NBA)."""

from __future__ import annotations

import httpx

from nba_api.constants import DEFAULT_BASE_URL, SPORT_KEY
from nba_api.exceptions import OddsApiError
from nba_api.models import NbaOddsEvent

_REQUEST_HEADERS_TO_FORWARD = ("x-requests-remaining", "x-requests-used")


def _filter_odds_headers(headers: httpx.Headers) -> dict[str, str]:
    return {
        k: v
        for k, v in headers.items()
        if k.lower() in {h.lower() for h in _REQUEST_HEADERS_TO_FORWARD}
    }


class OddsApiClient:
    """Sync client for NBA odds via The Odds API."""

    def __init__(
        self,
        api_key: str,
        base_url: str = DEFAULT_BASE_URL,
        *,
        timeout: float = 30.0,
        transport: httpx.BaseTransport | None = None,
    ):
        self._api_key = api_key
        self._base = base_url.rstrip("/")
        self._client = httpx.Client(timeout=timeout, transport=transport)

    def close(self) -> None:
        self._client.close()

    def __enter__(self) -> OddsApiClient:
        return self

    def __exit__(self, *args: object) -> None:
        self.close()

    def _request_json(self, path: str, params: dict[str, str]) -> tuple[list | dict, dict[str, str]]:
        url = f"{self._base}{path}"
        q = {"apiKey": self._api_key, **params}
        try:
            r = self._client.get(url, params=q)
        except httpx.RequestError as e:
            raise OddsApiError(f"Odds API request failed: {e}") from e

        odds_headers = _filter_odds_headers(r.headers)
        if r.status_code >= 400:
            body = (r.text or "")[:500]
            raise OddsApiError(
                f"Odds API HTTP {r.status_code}",
                status_code=r.status_code,
                body=body,
            )

        try:
            data = r.json()
        except ValueError as e:
            raise OddsApiError("Odds API returned non-JSON body", status_code=r.status_code) from e

        return data, odds_headers

    def get_nba_odds(
        self,
        *,
        regions: str,
        markets: str,
        odds_format: str = "american",
    ) -> tuple[list[NbaOddsEvent], dict[str, str]]:
        """
        GET /v4/sports/basketball_nba/odds — upcoming games with bookmaker lines.

        :param regions: e.g. ``us`` (comma-separated allowed by API)
        :param markets: e.g. ``h2h,spreads,totals``
        """
        path = f"/sports/{SPORT_KEY}/odds"
        data, headers = self._request_json(
            path,
            {
                "regions": regions,
                "markets": markets,
                "oddsFormat": odds_format,
            },
        )
        if not isinstance(data, list):
            raise OddsApiError("Expected JSON array from /odds", status_code=200)
        return data, headers

    def get_nba_event_odds(
        self,
        event_id: str,
        *,
        regions: str,
        markets: str,
        odds_format: str = "american",
    ) -> tuple[dict, dict[str, str]]:
        """
        GET /v4/sports/basketball_nba/events/{eventId}/odds — per-event markets (e.g. player props).

        :param markets: comma-separated keys, e.g. ``player_points,player_rebounds``
        """
        path = f"/sports/{SPORT_KEY}/events/{event_id}/odds"
        data, headers = self._request_json(
            path,
            {
                "regions": regions,
                "markets": markets,
                "oddsFormat": odds_format,
            },
        )
        if not isinstance(data, dict):
            raise OddsApiError("Expected JSON object from /events/.../odds", status_code=200)
        return data, headers
