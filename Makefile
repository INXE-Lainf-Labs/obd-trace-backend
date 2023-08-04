help:
	@echo "Usage: make [run|docker-up|docker-up-db|install-code-formatter|test|coverage-test|lint|lint-fix]"
	@echo
	@echo 'Usage:'
	@echo '    make docker-up       							Run Docker container.'
	@echo '    make docker-up-db       							Run Database in Docker.'
	@echo '    make docker-prune       							Delete project containers, images and volumes.'
	@echo '    make docker-reload       						Shortcut for docker-prune and docker-up targets.'
	@echo '    make install-code-formatter						Install code formatter.'
	@echo '    make test            							Run tests on the project.'
	@echo '    make coverage-test       						Run tests on the project and generates a coverage report.'
	@echo '    make coverage-test-local     					Run tests on the project and generates a HTML coverage report locally without docker.'
	@echo '    make lint			 							Runs the linter checker.'
	@echo '    make lint-fix									Try to fix lint erros.'
	@echo '    make new-feature FEAT_NAME=<name>				Shortcut to create new feature files in the project structure.'
	@echo '    make clean-migration MIGRATION_TITLE=<title>		Shortcut to downgrade migration to base, delete files from project structure, create a new revision, and upgrade to head.'
	@echo '    make new-migration MIGRATION_TITLE=<title>		Shortcut to create a new revision, and upgrade to head.'
	@echo

docker-up:
	docker-compose up

docker-up-db:
	docker-compose up db

docker-prune:
	docker-compose down
	docker rmi "$(notdir $(PWD))-backend" "$(notdir $(PWD))-backend-init"
	docker volume rm "$(notdir $(PWD))_pg-data"

docker-reload: docker-prune docker-up

install-code-formatter:
	pip install -r src/config/requirements/dev.txt
	pre-commit install

test:
	docker exec -it backend pip install -r src/config/requirements/test.txt
	docker exec -it backend python -m pytest

coverage-test:
	docker exec -it backend pytest --cov=./ --cov-report=xml

coverage-test-local:
	pytest --cov=./ --cov-report=html

lint:
	black --check ./src

lint-fix:
	black ./src

new-feature:
	@echo Creating files...
	@mkdir ./src/$(FEAT_NAME)
	@touch ./src/$(FEAT_NAME)/__init__.py
	@mkdir ./src/$(FEAT_NAME)/test
	@touch ./src/$(FEAT_NAME)/test/__init__.py
	@mkdir ./src/$(FEAT_NAME)/v1
	@touch ./src/$(FEAT_NAME)/v1/__init__.py
	@touch ./src/$(FEAT_NAME)/v1/routes.py
	@touch ./src/$(FEAT_NAME)/exceptions.py
	@touch ./src/$(FEAT_NAME)/schemas.py
	@touch ./src/$(FEAT_NAME)/services.py
	@touch ./src/$(FEAT_NAME)/models.py
	@echo Done!

clean-migration:
	@alembic downgrade base
	@rm -rf src/config/database/migrations/versions/*
	@alembic revision --autogenerate -m "$(MIGRATION_TITLE)"
	@alembic upgrade head

new-migration:
	@alembic revision --autogenerate -m "$(MIGRATION_TITLE)"
	@alembic upgrade head
