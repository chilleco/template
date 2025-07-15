# Makefile at repo-root
ENV_FILE ?= .env.local

up:        ## Запустить весь стек (dev)
	ENV_FILE=$(ENV_FILE) docker compose up -d

build:     ## Пересобрать контейнеры
	ENV_FILE=$(ENV_FILE) docker compose build

logs:      ## Хвост логов backend + frontend
	docker compose logs -f backend frontend

down:      ## Остановить и удалить контейнеры (без volumes)
	docker compose down

clean:     ## Полный reset окружения
	docker compose down -v --remove-orphans
	docker system prune -f

test:      ## Локально прогнать тесты в контейнерах
	docker compose -f infra/compose/docker-compose.yml \
	               -f infra/compose/docker-compose.test.yml \
	               up --build --abort-on-container-exit --exit-code-from backend
