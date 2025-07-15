"""APScheduler singleton used by the application."""

from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from structlog import get_logger

from app.tasks.jobs import send_welcome_email

scheduler = AsyncIOScheduler(timezone="UTC")
log = get_logger()

# Every day at 02:00 UTC clean up inactive users (example)
@scheduler.scheduled_job(
    CronTrigger(hour=2, minute=0, second=0),
    name="daily_cleanup",
)
def _cleanup_job() -> None:
    log.info("daily_cleanup_started")
    # enqueue real async task or run sync maintenance
    send_welcome_email.delay("system")  # demo action
