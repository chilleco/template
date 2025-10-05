from __future__ import annotations

from arq import cron
from arq.connections import RedisSettings

from app.core.settings import settings
from app.tasks.cleanup_sessions import task as cleanup_sessions
from app.tasks.notify_user import task as notify_user
from app.tasks.poll_external import task as poll_external


async def startup(ctx):  # pragma: no cover - executed by arq runtime
    ctx["settings"] = settings


async def shutdown(ctx):  # pragma: no cover
    ctx.clear()


class WorkerSettings:
    redis_settings = RedisSettings.from_dsn(settings.redis_url)
    on_startup = startup
    on_shutdown = shutdown
    functions = [cleanup_sessions, notify_user, poll_external]
    cron_jobs = [cron(cleanup_sessions, minute=0)]
