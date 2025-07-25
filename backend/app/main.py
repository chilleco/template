"""FastAPI application bootstrap."""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.logging import logger 
from app.core.settings import Settings, get_settings
from app.core.dependencies import lifespan_context
from app.api.v1 import api_v1_router
from app.cron.scheduler import scheduler

settings: Settings = get_settings()     # single-instance
logger.info("app_bootstrap", env=settings.env)

app = FastAPI(
    title="My Awesome API",
    version="1.0.0",
    lifespan=lifespan_context,          # graceful startup/shutdown
)

# CORS (example: allow swagger in dev)
if settings.env.lower() != "prod":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.include_router(api_v1_router, prefix="/api/v1")

# start APScheduler after app startup
@app.on_event("startup")
async def _start_scheduler() -> None:
    scheduler.start(paused=False)
