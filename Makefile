help:
	@echo "Usage: make [run|docker-up|docker-up-db|install-code-formatter|test|coverage-test|lint|lint-fix]"
	@echo
	@echo 'Usage:'
	@echo '    make docker-up       		Run Docker container.'
	@echo '    make docker-up-db       		Run Database in Docker.'
	@echo '    make docker-prune       		Delete project containers, images and volumes.'
	@echo '    make docker-reload       	Shortcut for docker-prune and docker-up targets.'
	@echo '    make install-code-formatter	Install code formatter.'
	@echo '    make test            		Run tests on the project.'
	@echo '    make coverage-test       	Run tests on the project and generates a coverage report.'
	@echo '    make lint			 		Runs the linter checker.'
	@echo '    make lint-fix				Try to fix lint erros.'
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

lint:
	black --check ./src

lint-fix:
	black ./src
