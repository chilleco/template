from celery import Celery
import requests
from ..config import settings

celery_app = Celery("myapp", broker=settings.redis_url, backend=settings.redis_url)

@celery_app.task(name="send_email")
def send_email_task(to_email: str, subject: str, body: str):
    # Пример: отправка email через сторонний сервис
    # Здесь можно вызвать SMTP или внешнее API почтового сервиса
    print(f"Sending email to {to_email}: {subject}")

@celery_app.task(name="generate_report")
def generate_report_task():
    # Пример длительной задачи: генерация финансового отчёта
    # ... сбор данных из БД, агрегация, сохранение отчета
    print("Report generated")

# Планирование задач (например, ежедневные отчёты)
from celery.schedules import crontab
celery_app.conf.beat_schedule = {
    'daily-report': {
        'task': 'generate_report',
        'schedule': crontab(hour=0, minute=0),  # каждый день в полночь
    },
}
