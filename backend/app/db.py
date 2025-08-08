# backend/app/db.py
import os
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import sessionmaker, Session

DATABASE_URL = os.getenv("DATABASE_URL")  # e.g., "postgresql+asyncpg://user:pass@host/dbname"
# If we have a read replica URL, we could get it from env too
DATABASE_RW_URL = os.getenv("DATABASE_RW_URL", DATABASE_URL)
DATABASE_RO_URL = os.getenv("DATABASE_RO_URL")  # optional read-only replica

# Create engine for write operations (and default)
engine = create_async_engine(DATABASE_RW_URL, pool_size=20, max_overflow=0)
# If a separate read engine is provided:
read_engine = create_async_engine(DATABASE_RO_URL, pool_size=20, max_overflow=0) if DATABASE_RO_URL else None

# Session maker for dependency injection
AsyncSessionLocal = async_sessionmaker(bind=engine, expire_on_commit=False)
AsyncReadSessionLocal = async_sessionmaker(bind=read_engine, expire_on_commit=False) if read_engine else AsyncSessionLocal

async def get_session(read_only: bool = False) -> AsyncSessionLocal:
    """Yield an async DB session. If read_only and a read replica is configured, use that."""
    async with (AsyncReadSessionLocal() if read_only and read_engine else AsyncSessionLocal()) as session:
        yield session
