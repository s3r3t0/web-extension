# Contributing

## Prerequisites

- Python 3.12+
- uv
- Make
- Firefox (for extension manual validation)

## Local setup

1. Clone the repository.
2. Bootstrap the local environment:

```bash
make bootstrap
```

1. Install the pre-commit Git hook:

```bash
make precommit-install
```

1. For parent-domain and subdomain cookie scenarios, map test hosts locally:

```text
127.0.0.1 app.localtest.me
127.0.0.1 api.localtest.me
```

1. Run the cookie lab app:

```bash
make run-https
```

1. Open the app in your browser:

- <https://app.localtest.me:8443>
- <https://api.localtest.me:8443>

## Development commands

- Sync dependencies: `make sync`
- Lock dependency graph: `make lock`
- Run lint checks: `make lint`
- Run type checks: `make typecheck`
- Check formatting: `make format-check`
- Auto-format: `make format`
- Run Python tests on the active interpreter: `make test`
- Scenario tests only: `make test-scenarios`
- Coverage run: `make test-coverage`
- Install E2E browsers: `make test-e2e-install`
- Install browsers for optional checks: `make test-optional-install`
- E2E smoke (Chromium + Firefox): `make test-e2e`
- E2E smoke (Chromium): `make test-e2e-chromium`
- E2E smoke (Firefox): `make test-e2e-firefox`
- Runtime popup E2E: `make test-e2e-runtime`
- Run all pre-commit hooks: `make precommit`
- Local required CI checks: `make ci-local`
- Local optional CI checks: `make ci-optional`

`make ci-local` runs pre-commit and a strict documentation build once, Python
tests on 3.12, 3.13, and 3.14, then browser smoke tests on the active
interpreter. It installs the Playwright browser binaries, but not system
dependencies. On Linux, if needed, install those using
`make test-e2e-install PLAYWRIGHT_INSTALL_ARGS=--with-deps` (or
`make test-optional-install PLAYWRIGHT_INSTALL_ARGS=--with-deps` for optional checks).
The Python matrix fails rather than silently skipping a missing interpreter.
Browser tests need the host mapping above and port 8443 available.

`make ci-optional` runs coverage (including browser smoke tests) and the
extension runtime tests, installing the browser versions required by those tox
environments. The runtime tests may report skips when Chromium cannot load the
extension; a successful command alone does not guarantee they ran.
Coverage measures the pytest process, not the Flask subprocess used by browser
tests.
`E2E_BROWSERS`, `E2E_HEADLESS`, and `COOKIE_LAB_BASE_URL` are passed into tox
for the applicable browser tests.

The pre-commit hooks use the `uv.lock` dependencies. Tox installs its own
environment dependencies from the version ranges in `pyproject.toml`, so they
are not guaranteed to match the lockfile. Browser installation uses the E2E
tox environment's Playwright version.

## Documentation conventions

- Keep extension and testing-app sections separate.
- Keep scenario IDs stable once published.
- Update docs/testing-app/scenarios.md when scenario list changes.
- Update docs/testing-app/coverage-matrix.md when coverage status changes.

## CI setup and maintenance

CI installs uv using the official `astral-sh/setup-uv` action, pinned by commit
SHA. The workflow currently selects `latest-known` for uv.
Branch protection should require the quality, Python matrix, and browser smoke
checks; the coverage and runtime job is optional. Update required check names
in repository settings when changing the workflow jobs.

### Why this setup

- Uses the upstream recommended GitHub integration for uv.
- Keeps bootstrap behavior consistent across jobs.
- Preserves supply-chain hardening by pinning action commit SHAs.

### Pinning policy

- Pin GitHub actions by full commit SHA.
- Pin the uv version explicitly via the setup action `version` input when adopting a fixed version.
- Avoid floating installs such as `pip install --upgrade uv` in workflows.

### Update policy

1. Update the `astral-sh/setup-uv` action reference in `.github/workflows/ci.yml` to the desired pinned SHA.
2. Update the uv `version` value in the same workflow if changing the selected version.
3. Run local checks (`make ci-local`) before opening the PR.
4. Ensure GitHub Actions CI is green before merge.

### Dependabot expectations

- `github-actions` updates in `.github/dependabot.yml` can propose updates for `uses:` action references.
- The uv version in `with: version:` is controlled separately from action updates.

## Workflow

1. Edit docs.
2. Run make docs-build.
3. Run make docs-check.
4. Include documentation updates in the same PR as code changes.
5. Use Ruff and ty for Python quality checks; pre-commit should stay aligned with `make lint` and `make typecheck`.
