"""Lightweight types for Odds API JSON (extend as needed)."""

from typing import Any

# The Odds API returns a list of game objects for /odds; each has id, sport_key, commence_time,
# home_team, away_team, bookmakers, etc.
NbaOddsEvent = dict[str, Any]
