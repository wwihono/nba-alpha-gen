# NBA Alpha Gen

[![CI](https://github.com/wwihono/nba-alpha-gen/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/wwihono/nba-alpha-gen/actions/workflows/ci.yml)

**NBA Alpha Gen** is a research-oriented **sports betting edge dashboard** for the NBA. It is designed to combine **schedule and player data**, **injury intelligence**, **multi-book player-prop line tracking** (“line scalping”), **machine-learning signals**, **risk tiers**, **daily picks / locks**, **favorite players**, **automatic blacklisting** after consecutive prop misses, and **game-level context** (home court, head-to-head, defensive matchup notes, momentum, optional Monte Carlo simulation). The product is **decision-support only**—not financial advice and not a betting execution service.

This repository is **under active development**. It includes a **FastAPI** backend and a **Vite + React** dashboard under `frontend/` (navy-forward **light/dark** UI, spec-aligned sections). Live odds ingestion and ML layers follow the phased roadmap.

---

## What this app does (brief)

| Area | Intent |
|------|--------|
| **Data** | Normalize NBA schedules, players, injuries, and (later) odds snapshots from licensed or public APIs per their terms. |
| **Player props** | Track lines across books, surface movement, best price, and model vs. market edge. |
| **Risk & picks** | Label risk per line; rank daily picks and “lock” tiers with auditable metadata. |
| **Personalization** | Favorite players; auto-hide recommendations for players who miss tracked props **3+ games in a row** (with overrides in settings). |
| **Game view** | Home court, H2H, schemes/matchup context, streaks, optional **100-game** simulation for suggested margin/spread vs. market. |
| **UI** | Navy-forward brand with **light** and **dark** themes (`frontend/`, calls the API via `VITE_API_URL`). |

---

## Requirements

- **Python 3.11+** (3.12 recommended)
- **pip** (or another PEP 517 installer)
- **Git** (to clone the repository)

- **Node.js 20+** and **npm** — for the `frontend/` dashboard (`npm install`, `npm run dev`).  
Optional later: PostgreSQL for persistence, API keys for odds and stats providers.

---

## Installation

### 1. Clone the repository

```bash
git clone <your-fork-or-remote-url>
cd nba-alpha-gen
```

### 2. Create and activate a virtual environment

**Windows (PowerShell)**

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

**macOS / Linux**

```bash
python3 -m venv .venv
source .venv/bin/activate
```

### 3. Install the package in editable mode

```bash
pip install --upgrade pip
pip install -e .
```

For development tools (tests, linter):

```bash
pip install -e ".[dev]"
```

---

## Configuration (environment variables)

Optional variables use the prefix **`NBA_`**. You can place them in a **`.env`** file in the project root (do not commit secrets).

| Variable | Default | Purpose |
|----------|---------|---------|
| `NBA_APP_NAME` | `NBA Alpha Gen` | Display name in API metadata. |
| `NBA_DEBUG` | `false` | Reserved for verbose logging / dev behavior. |
| `NBA_CORS_ORIGINS` | includes `localhost:3000`, `127.0.0.1:3000`, **`5173`** (Vite) | Comma-separated origins allowed for browser calls to the API. |

Example **`.env`** (create manually):

```env
NBA_DEBUG=false
NBA_CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:5173
```

---

## Running the application

From the **project root**, with the virtual environment **activated**:

```bash
uvicorn nba_alpha_gen.main:app --reload --host 127.0.0.1 --port 8000
```

**Windows PowerShell** (same command):

```powershell
uvicorn nba_alpha_gen.main:app --reload --host 127.0.0.1 --port 8000
```

You should see Uvicorn listening on `http://127.0.0.1:8000`.

---

## Web dashboard (frontend)

From the repo root:

```bash
cd frontend
cp .env.example .env
npm install
npm run dev
```

Open **http://localhost:5173**. The UI expects the API at **`VITE_API_URL`** (default `http://127.0.0.1:8000` in `.env`). Run **Uvicorn** in a separate terminal so the status bar can reach `/health` and `/api/v1/info`.

- **Dashboard** — Slate, game analysis, injuries, prop board, picks, reports, data health (mock or placeholder until backends exist).  
- **Favorites** — Local list of players (browser-only for now).  
- **Settings** — Theme note, blacklist placeholder, API env hint.  
- **Theme** — Toggle in the header (**Light** / **Dark**); preference is stored in `localStorage`.

Production build: `npm run build` (output in `frontend/dist/`).

---

## How to use the API (current build)

### Interactive documentation

Open a browser:

- **Swagger UI:** [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)  
- **ReDoc:** [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

### Endpoints available today

| Method | Path | Description |
|--------|------|-------------|
| `GET` | `/health` | Liveness check; returns `{"status":"ok"}`. |
| `GET` | `/api/v1/info` | API name, version, and link to docs. |

Example with **curl**:

```bash
curl http://127.0.0.1:8000/health
curl http://127.0.0.1:8000/api/v1/info
```

When the **web UI** is added, point it at this API base URL (same host/port or proxied). Keep `NBA_CORS_ORIGINS` aligned with the UI dev server origin.

---

## User workflow (target product — as features land)

These steps describe how the **finished product** is meant to be used; many pieces are **not implemented yet** and will appear release by release.

1. **Open the dashboard** — Choose **light** or **dark** theme; primary navigation uses a **navy** base in both modes.  
2. **Review the slate** — See upcoming games, start times, and team **win/loss streak** badges where available.  
3. **Open a game** — Read **home court** context, **H2H** history, **defensive matchup** notes, and **momentum**. Optionally run the **100-game simulation** to compare **model margin** to the market **spread**.  
4. **Browse player props** — Line board shows **best line**, **movement**, **risk** tier, and **steam** flags from **scalped** odds snapshots.  
5. **Filter** — Restrict by **risk** level and by **pick vs. lock** tier; use **“show hidden”** to include **auto-blacklisted** players (missed tracked props **3+** straight games after grading).  
6. **Favorites** — Add players you track; use **favorites-first** sorting when enabled. Blacklisted players stay out of **main** recommendations unless you change settings.  
7. **Reasoning & reports** — Open a line or pick for **structured reasoning** (market path, injuries, usage, model vs. market). Export **daily** or **per-game** HTML/PDF when implemented.  
8. **Compliance** — Treat all picks and simulations as **probabilistic**; “locks” are **internal tiers**, not guarantees. Obey local laws and sportsbook terms.

---

## Project layout

```
nba-alpha-gen/
├── README.md                 # This file
├── pyproject.toml            # Python package and dependencies
├── src/nba_alpha_gen/
│   ├── main.py               # FastAPI app
│   └── config.py             # Settings (env-backed)
├── tests/                    # pytest (see Development)
├── frontend/                 # Vite + React dashboard
├── .github/workflows/ci.yml  # GitHub Actions: pytest + frontend build
└── .gitignore
```

Additional folders (`data/`, `models/`, `docs/`) may appear as ingestion and ML work land.

---

## Development

### Lint (optional)

```bash
ruff check src
```

### Run tests

Install dev dependencies: `pip install -e ".[dev]"`.

```bash
pytest -v
```

Tests live under `tests/` and cover `GET /health`, `GET /api/v1/info`, OpenAPI, `/docs`, error codes, and CORS (see `tests/test_api.py`).

### Continuous integration

On every **push** and **pull request** to `main` (or `master`), [GitHub Actions](.github/workflows/ci.yml) runs **`pytest`** on **Python 3.11 and 3.12** and **`npm ci` + `npm run build`** in `frontend/` (Node 20). You can also run the workflow manually from the Actions tab (**workflow_dispatch**).

If the badge above shows “failing” or the link 404s, update the repo path in the badge URL to match your GitHub remote.

---

## Legal and responsible use

Sports betting is **regulated or prohibited** in many jurisdictions. This software is for **research and informational purposes**. It does **not** place bets, guarantee profit, or provide personalized financial advice. Use official data and odds **only** in compliance with each provider’s **Terms of Service**. If you gamble, do so legally and within your means.

---

## Roadmap (high level)

1. Persisted schema and NBA/stats ingestion.  
2. Injury pipeline and feature engineering.  
3. Multi-book prop odds snapshots and line board UI.  
4. ML, risk engine, picks/locks, reasoning exports.  
5. Favorites, grading, auto-blacklist, game-detail panels and Monte Carlo.  

See internal planning docs for phase detail.
