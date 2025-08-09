# Stage 1: сборка зависимостей и приложения
FROM python:3.13-slim AS builder

WORKDIR /app

# Установим зависимости
COPY requirements.txt .
# requirements.txt содержит только prod-зависимости; dev-зависимости (например, pytest) в requirements-dev.txt
RUN pip install --no-cache-dir -r requirements.txt

# Если есть компилируемые зависимости (C-библиотеки), можно установить build-base, а потом удалить, или использовать python:3.11 альпийский + apk.
# Здесь для простоты используем slim-базу и полагаемся на wheel пакеты.

COPY . .

# Stage 2: финальный образ
FROM python:3.13-slim AS final

WORKDIR /app

# Копируем requirements.txt и устанавливаем зависимости заново (проще и надежнее)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем приложение ( .py файлы )
COPY . .

# Создаем пользователя для запуска приложения (не root – best practice)
RUN useradd -m fastapi_user && chown -R fastapi_user /app
USER fastapi_user

# По умолчанию запускаем сервер (команду можно переопределить через compose при необходимости)
ENV PORT=8000
ENV PYTHONPATH=/app
EXPOSE 8000
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
