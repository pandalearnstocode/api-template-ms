path := .

define Comment
	- Run `make help` to see all the available options.
	- Run `make lint` to run the linter.
	- Run `make lint-check` to check linter conformity.
	- Run `dep-lock` to lock the deps in 'requirements.txt' and 'requirements-dev.txt'.
	- Run `dep-sync` to sync current environment up to date with the locked deps.
endef


.PHONY: lint
lint: black isort flake mypy	## Apply all the linters.


.PHONY: lint-check
lint-check:  ## Check whether the codebase satisfies the linter rules.
	@echo
	@echo "Checking linter rules..."
	@echo "========================"
	@echo
	@black --check $(path)
	@isort --check $(path)
	@flake8 $(path)
	@mypy $(path)


.PHONY: black
black: ## Apply black.
	@echo
	@echo "Applying black..."
	@echo "================="
	@echo
	@black --fast $(path)
	@echo


.PHONY: isort
isort: ## Apply isort.
	@echo "Applying isort..."
	@echo "================="
	@echo
	@isort $(path)


.PHONY: flake
flake: ## Apply flake8.
	@echo
	@echo "Applying flake8..."
	@echo "================="
	@echo
	@flake8 $(path)


.PHONY: mypy
mypy: ## Apply mypy.
	@echo
	@echo "Applying mypy..."
	@echo "================="
	@echo
	@mypy $(path)

.PHONY: auto-format
auto-format: ## Apply auto-format.
	black .
	autopep8 --exit-code --recursive --in-place --aggressive --aggressive .
	autoflake --in-place -r --ignore-init-module-imports --remove-unused-variables --remove-all-unused-imports .

.PHONY: generate-lint-reports
 generate-lint-reports: ##  generate-lint-reports
	bandit --exit-zero --format json --output bandit-report.json --recursive .
	pylint . --exit-zero > pylint-report.out
	flake8 --exit-zero --output-file=flake8.txt .
	pylint app -r n --msg-template="{path}:{line}: [{msg_id}({symbol}), {obj}] {msg}" --exit-zero > pylint.log

.PHONY: help
help: ## Show this help message.
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: test
test: ## Run the tests against the current version of Python.
	pytest


.PHONY: dep-lock
dep-lock: ## Freeze deps in 'requirements.txt' file.
	@pip-compile requirements.in -o requirements.txt
	@pip-compile requirements-dev.in -o requirements-dev.txt


.PHONY: dep-sync
dep-sync: ## Sync venv installation with 'requirements.txt' file.
	@pip-sync

.PHONY: dep-update
dep-update: ## Update all the deps.
	@chmod +x ./scripts/update_deps.sh
	@./scripts/update_deps.sh


.PHONY: build-docker-images
build-docker-images: ## Run this to build docker images
	docker-compose -f docker-compose.staging.yml build


.PHONY: run-container-dev
run-container-dev: ## Run the app in a docker container.
	docker-compose -f docker-compose.dev.yml up -d

.PHONY: kill-container-dev
kill-container-dev: ## Stop the running docker container.
	docker-compose -f docker-compose.dev.yml down

.PHONY: run-container-staging
run-container-staging: ## Run the app in a docker container.
	docker-compose -f docker-compose.staging.yml up -d

.PHONY: kill-container-staging
kill-container-staging: ## Stop the running docker container.
	docker-compose -f docker-compose.staging.yml down


.PHONY: run-local
run-local: ## Run the app locally.
	python -m uvicorn app.main:app --port 5000 --reload

.PHONY: bump
bump: ## Bump library version.
	cz bump --changelog --check-consistency
	git push --tags

.PHONY: commit-push
commit-push: ## Commit and push changes.
	git add .
	cz -n cz_commitizen_emoji c
	git push origin develop

.PHONY: wiki-generate
wiki-generate: ## Generate the wiki.
	mkdocs build
	mkdocs serve

.PHONY: wiki-clean
wiki-clean:	## Clean the wiki.
	rm -rf site/

.PHONY: wiki-publish-gh
wiki-publish-gh: ## Publish the wiki to GitHub Pages. 
	mkdocs build
	mkdocs gh-deploy
	rm -rf site/

.PHONY: clean
clean:            ## Clean unused files.
	@find ./ -name '*.pyc' -exec rm -f {} \;
	@find ./ -name '__pycache__' -exec rm -rf {} \;
	@find ./ -name 'Thumbs.db' -exec rm -f {} \;
	@find ./ -name '*~' -exec rm -f {} \;
	@rm -rf .cache
	@rm -rf .pytest_cache
	@rm -rf .mypy_cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build


