"""Asynchronous background / Celery tasks."""

from celery import shared_task
from structlog import get_logger

log = get_logger()

@shared_task(name="email.send_welcome")
def send_welcome_email(user_id: str) -> None:
    # imagine SMTP or 3-rd party email API here
    log.info("send_welcome_email", user_id=user_id)
