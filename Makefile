UV ?= uv
PYTHON ?= python3
APP_MODULE ?= cookie_lab.__main__
APP_HOST ?= 0.0.0.0
APP_HTTP_PORT ?= 8000
APP_HTTPS_PORT ?= 8443

.PHONY: bootstrap sync lock clean run-http run-https test test-scenarios test-coverage docs-serve docs-build docs-check lint format-check precommit ci-local

bootstrap:
	$(UV) sync --group dev --group docs --group lint --group test

sync:
	$(UV) sync --group dev --group docs --group lint --group test

lock:
	$(UV) lock

clean:
	rm -rf .pytest_cache .ruff_cache site

run-http:
	$(UV) run flask --app cookie_lab.app:create_app run --host $(APP_HOST) --port $(APP_HTTP_PORT)

run-https:
	$(UV) run flask --app cookie_lab.app:create_app run --host $(APP_HOST) --port $(APP_HTTPS_PORT) --cert adhoc

test:
	$(UV) run --group test pytest

test-scenarios:
	$(UV) run --group test pytest tests/test_scenarios.py

test-coverage:
	$(UV) run --group test pytest --cov=cookie_lab --cov-report=term-missing

docs-serve:
	$(UV) run --group docs zensical serve

docs-build:
	$(UV) run --group docs zensical build

docs-check:
	$(UV) run --group docs zensical build --strict

lint:
	$(UV) run --group lint ruff check .

format-check:
	$(UV) run --group lint ruff format --check .

precommit:
	$(UV) run --group dev pre-commit run --all-files

ci-local: lint format-check test docs-build
