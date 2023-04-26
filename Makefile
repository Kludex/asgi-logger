.PHONY: help
help: ## Show this help
	@egrep -h '\s##\s' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


.PHONY: install
install:  ## Install package
	@echo "🏗️ Install package"
	python -m pip install --upgrade pip
	python -m pip install --upgrade poetry==1.3.0
	poetry install


.PHONY: lint
lint:  ## Linter the code.
	@echo "🚨 Linting code"
	poetry run isort asgi_logger tests --check
	poetry run flake8 asgi_logger tests
	poetry run mypy asgi_logger
	poetry run black asgi_logger tests --check --diff


.PHONY: format
format:
	@echo "🎨 Formatting code"
	poetry run isort asgi_logger tests
	poetry run autoflake --remove-all-unused-imports --recursive --remove-unused-variables --in-place asgi_logger tests --exclude=__init__.py
	poetry run black asgi_logger tests


.PHONY: test
test:  ## Test your code.
	@echo "🍜 Running pytest"
	poetry run pytest -vv tests/ --cov=asgi_logger --cov-report=term-missing:skip-covered --cov-report=xml --cov-fail-under 100


.PHONY: publish
publish:  ## Publish release to PyPI
	@echo "🔖 Publish to PyPI"
	poetry config http-basic.pypi "__token__" "${POETRY_PYPI_TOKEN_PYPI}"
	poetry publish --build
