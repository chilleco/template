SHELL := /usr/bin/env bash
.ONESHELL:
.DEFAULT_GOAL := help

# ==== Paths ====
COMPOSE_BASE := infra/compose/compose.yml
COMPOSE_LOCAL := infra/compose/compose.local.yml
COMPOSE_DEV := infra/compose/stack.dev.yml
COMPOSE_PROD := infra/compose/stack.prod.yml
TRAEFIK_STACK := infra/compose/stack.traefik.yml

# ==== Envs ====
ENV_FILE ?= .env

# ==== Helpers ====
define source_env
set -euo pipefail; \
if [[ -f $(1) ]]; then \
  set -a; source $(1); set +a; \
else \
  echo "ENV file $(1) not found"; exit 1; \
fi
endef

# ==== Help ====
help: ## Показать цели Makefile
	@grep -E '^[a-zA-Z0-9_-]+:.*?## ' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-18s\033[0m %s\n", $$1, $$2}'

# Export all variables from .env file
ifneq (,$(wildcard ./.env))
    include .env
    export
endif

# ==== Commands ====

up:
	docker compose \
		--env-file $(ENV_FILE) \
		-f $(COMPOSE_BASE) \
		-f $(COMPOSE_PROD) \
		up -d

up-dev:
	docker compose \
		--env-file $(ENV_FILE) \
		-f $(COMPOSE_BASE) \
		-f $(COMPOSE_DEV) \
		up -d

up-local:
	docker compose \
		--env-file $(ENV_FILE) \
		-f $(COMPOSE_BASE) \
		-f $(COMPOSE_LOCAL) \
		up -d

deploy-dev:
	. $(ENV_FILE); docker stack deploy \
		-c $(COMPOSE_BASE) \
		-c $(COMPOSE_DEV) \
	  	--with-registry-auth app-dev

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
