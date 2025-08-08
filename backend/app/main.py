from fastapi import FastAPI
from .config import settings
from .api import auth, posts, payments
import logging

app = FastAPI(title="My FinApp", version="1.0")

# Инициализация логирования (структурированный вывод JSON в stdout)
logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(message)s')

# Подключение роутеров (с префиксами)
app.include_router(auth.router, prefix="/auth")
app.include_router(posts.router, prefix="/posts", dependencies=[]) 
app.include_router(payments.router, prefix="/payments")

# Пример события запуска: подключение к БД, инициализация, миграции
@app.on_event("startup")
async def startup_event():
    # Подключение к базе данных, проверка соединения
    # Выполнение миграций (например, через Alembic)
    logging.info("Application startup: database connected and migrations applied")

# Пример события остановки
@app.on_event("shutdown")
async def shutdown_event():
    logging.info("Application shutdown: closing connections")
