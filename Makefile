# Makefile at repo-root

# Export all variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

up:        ## Запустить весь стек (production mode - stable)
	docker-compose --env-file .env -f infra/compose/compose.yml up -d

up-dev:    ## Запустить весь стек (dev mode with volume mounts)
	docker compose \
		-f infra/compose/compose.yml \
		-f infra/compose/compose.dev.yml \
		-f compose.local.yml \
		up -d

build:     ## Пересобрать контейнеры (production)
	docker-compose --env-file .env -f infra/compose/compose.yml build

build-dev: ## Пересобрать контейнеры (dev mode)
	docker-compose --env-file .env -f infra/compose/compose.yml -f compose.override.yml build

logs:      ## Хвост логов backend + frontend (production)
	docker-compose --env-file .env -f infra/compose/compose.yml logs -f backend frontend

logs-dev:  ## Хвост логов backend + frontend (dev mode)
	docker-compose --env-file .env -f infra/compose/compose.yml -f compose.override.yml logs -f backend frontend

down:      ## Остановить и удалить контейнеры (production)
	docker-compose --env-file .env -f infra/compose/compose.yml down

down-dev:  ## Остановить dev режим
	docker-compose --env-file .env -f infra/compose/compose.yml -f compose.override.yml down

clean:     ## Полный reset окружения
	docker-compose --env-file .env -f infra/compose/compose.yml -f compose.override.yml down -v --remove-orphans
	docker system prune -f

test:      ## Локально прогнать тесты в контейнерах
	docker-compose -f infra/compose/compose.yml \
	               -f infra/compose/compose.test.yml \
	               up --build --abort-on-container-exit --exit-code-from backend

ts-client:
	poetry run python -m scripts.generate_ts_client --url http://localhost:8000/openapi.json

.PHONY: ts-client
