DC = docker compose
APP = app

MANAGE = python manage.py

.PHONY: help up build down logs migrate makemigrations test lint shell superuser


help:
	@echo "-------------------- COMMANDS --------------------"
	@echo "make up              - Start services"
	@echo "make build           - Rebuild containers"
	@echo "make down            - Stop services"
	@echo "make logs            - View logs"
	@echo "-------------------- DJANGO ----------------------"
	@echo "make migrate         - Apply migrations"
	@echo "make makemigrations  - Create migrations"
	@echo "make superuser       - Create superuser"
	@echo "make shell           - Enter Django shell"
	@echo "-------------------- QUALITY ---------------------"
	@echo "make test            - Run tests (Pytest)"
	@echo "make lint            - Check code (Ruff)"
	@echo "make format          - Format code (Ruff)"
	@echo "--------------------------------------------------"
up:
	$(DC) up -d

build:
	$(DC) up --build -d

down:
	$(DC) down

logs:
	$(DC) logs -f

migrate:
	$(DC) run --rm $(APP) $(MANAGE) migrate

makemigrations:
	$(DC) run --rm $(APP) $(MANAGE) makemigrations

superuser:
	$(DC) run --rm $(APP) $(MANAGE) createsuperuser

shell:
	$(DC) run --rm $(APP) $(MANAGE) shell

test:
	$(DC) run --rm $(APP) pytest

lint:
	$(DC) run --rm $(APP) ruff check .

format:
	$(DC) run --rm $(APP) ruff format .