# Contributing

## Prerequisites

- Python 3.11+
- uv
- Make
- Firefox (for extension manual validation)

## Local setup

1. Clone the repository.
2. Bootstrap the local environment:

```bash
make bootstrap
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
- Check formatting: `make format-check`
- Auto-format: `make format`
- Run tests: `make test`
- Scenario tests only: `make test-scenarios`
- Coverage run: `make test-coverage`
- Install E2E browsers: `make test-e2e-install`
- E2E smoke (Chromium + Firefox): `make test-e2e`
- E2E smoke (Chromium): `make test-e2e-chromium`
- E2E smoke (Firefox): `make test-e2e-firefox`
- Runtime popup E2E: `make test-e2e-runtime`
- Local CI baseline target: `make ci-local`

## Documentation conventions

- Keep extension and testing-app sections separate.
- Keep scenario IDs stable once published.
- Update docs/testing-app/scenarios.md when scenario list changes.
- Update docs/testing-app/coverage-matrix.md when coverage status changes.

## CI setup and maintenance

CI installs uv using the official `astral-sh/setup-uv` action, with both the action reference and uv version pinned in the workflow.

### Why this setup

- Uses the upstream recommended GitHub integration for uv.
- Keeps bootstrap behavior consistent across jobs.
- Preserves supply-chain hardening by pinning action commit SHAs.

### Pinning policy

- Pin GitHub actions by full commit SHA.
- Pin uv version explicitly via the setup action `version` input.
- Avoid floating installs such as `pip install --upgrade uv` in workflows.

### Update policy

1. Update the `astral-sh/setup-uv` action reference in `.github/workflows/ci.yml` to the desired pinned SHA.
2. Update the uv `version` value in the same workflow.
3. Run local checks (`make ci-local`) before opening the PR.
4. Ensure GitHub Actions CI is green before merge.

### Dependabot expectations

- `github-actions` updates in `.github/dependabot.yml` can propose updates for `uses:` action references.
- The uv version in `with: version:` is intentionally controlled and should be bumped manually.

## Workflow

1. Edit docs.
2. Run make docs-build.
3. Run make docs-check.
4. Include documentation updates in the same PR as code changes.
