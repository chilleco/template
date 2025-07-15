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
    client = AsyncIOMotorClient(settings.mongo_uri)
    # yield motor-client (Beanie uses it under the hood)
    yield client
    client.close()

def get_logger_dep():
    return get_logger()

@asynccontextmanager
async def lifespan_context(app):
    """Global startup → connect Beanie; shutdown → close."""
    settings = get_settings()
    mongo = AsyncIOMotorClient(settings.mongo_uri)
    await init_beanie(mongo.db_name, document_models=[User])
    log.info("mongo_connected")
    yield
    mongo.close()
    log.info("mongo_closed")
