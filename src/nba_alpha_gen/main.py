from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from nba_alpha_gen.config import get_settings
from nba_alpha_gen.routers.odds import router as odds_router


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


def create_app() -> FastAPI:
    settings = get_settings()
    app = FastAPI(
        title=settings.app_name,
        description=(
            "API for the NBA edge dashboard: schedules, props, risk tiers, picks, "
            "favorites, and game-level analysis. UI and data pipelines are built incrementally."
        ),
        version="0.1.0",
        lifespan=lifespan,
    )
    origins = [o.strip() for o in settings.cors_origins.split(",") if o.strip()]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=origins or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    @app.get("/health", tags=["system"])
    async def health():
        return {"status": "ok"}

    @app.get("/api/v1/info", tags=["system"])
    async def info():
        return {
            "name": settings.app_name,
            "version": "0.1.0",
            "docs": "/docs",
        }

    app.include_router(odds_router)

    return app


app = create_app()
