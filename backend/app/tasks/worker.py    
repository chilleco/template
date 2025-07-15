"""Celery entry-point (called in docker-worker)."""

import os
from celery import Celery
from app.core.settings import get_settings

settings = get_settings()
broker_url = settings.redis_url  # e.g. redis://redis:6379/0

celery_app = Celery(
    "myapp",
    broker=broker_url,
    backend=broker_url,          # simple Redis result backend
)

celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    task_default_queue="default",
    timezone="UTC",
)

# автозагрузка модулей с задачами
celery_app.autodiscover_tasks(["app.tasks"])
