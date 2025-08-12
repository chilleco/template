import os
from celery import Celery
from structlog import get_logger

logger = get_logger()
celery_app = Celery(__name__, broker=os.getenv("REDIS_URL", "redis://redis:6379/0"))

@celery_app.task(name="send_welcome_email")
def send_welcome_email(user_id: int):
    # fetch user from DB (synchronously, or via an async wrapper)
    # send email via SMTP or third-party service
    logger.bind(task="send_welcome_email").info(f"Sending welcome email to user {user_id}")
