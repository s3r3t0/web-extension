UV ?= uv
PYTHON ?= python3
APP_MODULE ?= cookie_lab.__main__
APP_HOST ?= 0.0.0.0
APP_HTTP_PORT ?= 8000
APP_HTTPS_PORT ?= 8443
PLAYWRIGHT_INSTALL_ARGS ?=

.PHONY: bootstrap sync lock clean run-http run-https test test-scenarios test-coverage test-e2e-install test-optional-install test-e2e test-e2e-chromium test-e2e-firefox test-e2e-runtime docs-serve docs-build docs-check lint typecheck format format-check precommit precommit-install ci-quality ci-test-matrix ci-local ci-optional

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
	$(UV) run --locked --group dev tox -e test

test-scenarios:
	$(UV) run --locked --group dev tox -e test -- tests/test_scenarios.py

test-coverage:
	$(UV) run --locked --group dev tox -e coverage

test-e2e-install:
	$(UV) run --locked --group dev tox exec -e e2e -- playwright install $(PLAYWRIGHT_INSTALL_ARGS) chromium firefox

test-optional-install:
	$(UV) run --locked --group dev tox exec -e coverage -- playwright install $(PLAYWRIGHT_INSTALL_ARGS) chromium firefox
	$(UV) run --locked --group dev tox exec -e runtime -- playwright install $(PLAYWRIGHT_INSTALL_ARGS) chromium

test-e2e:
	$(UV) run --locked --group dev tox -e e2e

test-e2e-chromium:
	E2E_BROWSERS=chromium $(UV) run --locked --group dev tox -e e2e

test-e2e-firefox:
	E2E_BROWSERS=firefox $(UV) run --locked --group dev tox -e e2e

test-e2e-runtime:
	$(UV) run --locked --group dev tox -e runtime

docs-serve:
	$(UV) run --group docs zensical serve

docs-build:
	$(UV) run --group docs zensical build

docs-check:
	$(UV) run --locked --group dev tox -e docs

lint:
	$(UV) run --locked --group dev tox exec -e precommit -- pre-commit run --all-files ruff-check

typecheck:
	$(UV) run --locked --group dev tox exec -e precommit -- pre-commit run --all-files ty-check

format-check:
	$(UV) run --locked --group dev tox exec -e precommit -- pre-commit run --all-files ruff-format

format:
	$(UV) run --locked --group dev tox -e format

precommit:
	$(UV) run --locked --group dev tox -e precommit

precommit-install:
	$(UV) run --locked --group dev pre-commit install

ci-quality: precommit docs-check

ci-test-matrix:
	$(UV) run --locked --group dev tox -e 3.12,3.13,3.14

ci-local:
	$(MAKE) ci-quality
	$(MAKE) ci-test-matrix
	$(MAKE) test-e2e-install
	$(MAKE) test-e2e

ci-optional:
	$(MAKE) test-optional-install
	$(MAKE) test-coverage
	$(MAKE) test-e2e-runtime
