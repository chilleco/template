from __future__ import annotations

from datetime import datetime, timezone

from sqlalchemy import delete

from app.core.database import AsyncSessionLocal
from app.tasks.base import ScheduledTask
from app.models.user import UserSession


class CleanupSessionsTask(ScheduledTask):
    name = "cleanup_sessions"
    cron = "0 * * * *"  # hourly

    async def run(self) -> int:
        async with AsyncSessionLocal() as session:
            stmt = delete(UserSession).where(UserSession.expires_at < datetime.now(timezone.utc))
            result = await session.execute(stmt)
            await session.commit()
            return result.rowcount or 0


task = CleanupSessionsTask()
