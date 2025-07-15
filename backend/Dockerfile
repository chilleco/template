# Stage 1: сборка зависимостей и приложения
FROM python:3.11-slim AS builder

WORKDIR /app

# Установим зависимости
COPY requirements.txt .
# requirements.txt содержит только prod-зависимости; dev-зависимости (например, pytest) в requirements-dev.txt
RUN pip install --no-cache-dir -r requirements.txt

# Если есть компилируемые зависимости (C-библиотеки), можно установить build-base, а потом удалить, или использовать python:3.11 альпийский + apk.
# Здесь для простоты используем slim-базу и полагаемся на wheel пакеты.

COPY . .  # копируем весь исходный код FastAPI в образ

# Stage 2: финальный образ
FROM python:3.11-slim AS final

WORKDIR /app
# Переносим зависимости из builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

# Копируем приложение ( .py файлы )
COPY --from=builder /app ./

# Создаем пользователя для запуска приложения (не root – best practice)
RUN useradd -m fastapi_user && chown -R fastapi_user /app
USER fastapi_user

# По умолчанию запускаем сервер (команду можно переопределить через compose при необходимости)
ENV PORT=8000
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
