# Variáveis dinâmicas
PYTHON_VERSION := $(shell python --version 2>&1 | cut -d ' ' -f2)
DOCKER_COMPOSE := $(shell docker compose version > /dev/null 2>&1 && echo "docker compose" || echo "docker-compose")
DOCKER_IMAGE := $(notdir $(PWD))-backend
MIGRATION_TIMESTAMP := $(shell date +"%Y%m%d%H%M%S")
OS := $(shell uname)

ifeq ($(OS), Linux)
	OS_MSG := "Sistema operacional detectado: Linux"
endif
ifeq ($(OS), Darwin)
	OS_MSG := "Sistema operacional detectado: macOS"
endif
ifeq ($(OS), Windows_NT)
	OS_MSG := "Sistema operacional detectado: Windows"
endif

help:
	@echo "Usage: make [run|docker-up|docker-up-db|install-code-formatter|test|coverage-test|lint|lint-fix]"
	@echo
	@echo "$(OS_MSG)"
	@echo
	@echo '    make docker-up                Run Docker container.'
	@echo '    make docker-up-db             Run Database in Docker.'
	@echo '    make docker-prune             Delete project containers, images, and volumes.'
	@echo '    make docker-reload            Shortcut for docker-prune and docker-up targets.'
	@echo '    make install-code-formatter   Install code formatter.'
	@echo '    make test                     Run tests on the project.'
	@echo '    make coverage-test            Run tests and generate a coverage report.'
	@echo '    make coverage-test-local      Generate a local HTML coverage report without Docker.'
	@echo '    make lint                     Runs the linter checker.'
	@echo '    make lint-fix                 Try to fix lint errors.'
	@echo '    make new-feature FEAT_NAME=<name>        Create new feature files in the project structure.'
	@echo '    make clean-migration MIGRATION_TITLE=<title>  Reset, clean, and recreate migrations.'
	@echo '    make new-migration MIGRATION_TITLE=<title>    Create a new migration revision and apply it.'
	@echo

docker-up:
	@echo "Subindo containers com $(DOCKER_COMPOSE)..."
	$(DOCKER_COMPOSE) up

docker-up-db:
	@echo "Subindo apenas o banco de dados com $(DOCKER_COMPOSE)..."
	$(DOCKER_COMPOSE) up db

docker-prune:
	@echo "Removendo containers..."
	$(DOCKER_COMPOSE) down
	@echo "Removendo imagens Docker..."
	docker rmi "$(DOCKER_IMAGE)" "$(DOCKER_IMAGE)-init" || true
	@echo "Removendo volumes..."
	docker volume rm "$(notdir $(PWD))_pg-data" || true
	@echo "Cleanup concluído!"

docker-reload: docker-prune docker-up

install-code-formatter:
	@echo "Detectando versão do Python: $(PYTHON_VERSION)"
	pip install -r src/config/requirements/dev.txt
	pre-commit install
	@echo "Code formatter instalado com sucesso!"

test:
	@echo "Instalando dependências de teste e executando testes..."
	docker exec -it backend pip install -r src/config/requirements/test.txt
	docker exec -it backend python -m pytest

coverage-test:
	@echo "Executando testes e gerando relatório de cobertura..."
	docker exec -it backend pytest --cov=./ --cov-report=xml

coverage-test-local:
	@echo "Gerando relatório de cobertura localmente..."
	pytest --cov=./ --cov-report=html

lint:
	@echo "Verificando o código com Black..."
	black --check ./src

lint-fix:
	@echo "Corrigindo erros de lint com Black..."
	black ./src

new-feature:
	@echo "Criando estrutura para nova feature: $(FEAT_NAME)..."
	@mkdir -p ./src/$(FEAT_NAME)/test
	@mkdir -p ./src/$(FEAT_NAME)/v1
	@touch ./src/$(FEAT_NAME)/__init__.py
	@touch ./src/$(FEAT_NAME)/test/__init__.py
	@touch ./src/$(FEAT_NAME)/v1/__init__.py
	@touch ./src/$(FEAT_NAME)/v1/routes.py
	@touch ./src/$(FEAT_NAME)/exceptions.py
	@touch ./src/$(FEAT_NAME)/schemas.py
	@touch ./src/$(FEAT_NAME)/services.py
	@touch ./src/$(FEAT_NAME)/models.py
	@echo "Feature $(FEAT_NAME) criada com sucesso!"

clean-migration:
	@echo "Resetando migrações..."
	alembic downgrade base
	@echo "Limpando arquivos antigos de migração..."
	rm -rf src/config/database/migrations/versions/*
	@echo "Criando nova migração: $(MIGRATION_TITLE)..."
	alembic revision --autogenerate -m "$(MIGRATION_TITLE)"
	alembic upgrade head
	@echo "Migração recriada com sucesso!"

new-migration:
	@echo "Criando nova migração com timestamp..."
	alembic revision --autogenerate -m "$(MIGRATION_TIMESTAMP)_$(MIGRATION_TITLE)"
	alembic upgrade head
	@echo "Nova migração aplicada com sucesso!"
