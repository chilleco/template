"""FastAPI Depends helpers & lifespan context."""

from contextlib import asynccontextmanager
from beanie import init_beanie
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import Depends
from structlog import get_logger

from app.core.settings import get_settings
from app.models.user import User  # example document

log = get_logger()

async def get_db():
    """Return Mongo client (lazy DI)."""
    settings = get_settings()
    client = AsyncIOMotorClient(settings.mongo_connection_uri)
    # yield motor-client (Beanie uses it under the hood)
    yield client
    client.close()

def get_logger_dep():
    return get_logger()

@asynccontextmanager
async def lifespan_context(app):
    """Global startup → connect Beanie; shutdown → close."""
    settings = get_settings()
    mongo = None
    try:
        mongo = AsyncIOMotorClient(settings.mongo_connection_uri, serverSelectionTimeoutMS=2000)
        await init_beanie(mongo[settings.mongo_dbname], document_models=[User])
        log.info("mongo_connected")
    except Exception as exc:  # noqa: BLE001 - startup must not crash
        log.warning("mongo_connect_failed", error=str(exc))
        mongo = None
    yield
    if mongo:
        mongo.close()
        log.info("mongo_closed")
