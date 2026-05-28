# SeReTo Helper Web Extension

<picture>
  <source media="(prefers-color-scheme: dark)" srcset="https://raw.githubusercontent.com/s3r3t0/sereto/main/docs/assets/logo/sereto_block_white.svg">
  <source media="(prefers-color-scheme: light)" srcset="https://raw.githubusercontent.com/s3r3t0/sereto/main/docs/assets/logo/sereto_block_black.svg">
  <img src="https://raw.githubusercontent.com/s3r3t0/sereto/main/docs/assets/logo/sereto_block_black.svg" alt="SeReTo logo" align="right" height="150"/>
</picture>

[![GitHub release](https://img.shields.io/github/v/release/s3r3t0/web-extension)][release]
[![GitHub release date](https://img.shields.io/github/release-date/s3r3t0/web-extension)][release]
[![GitHub last commit](https://img.shields.io/github/last-commit/s3r3t0/web-extension)](https://github.com/s3r3t0/web-extension/commit/main)

[![Documentation](https://img.shields.io/badge/documentation-SeReTo-blue)](https://sereto.s4n.cz/)
[![GitHub License](https://img.shields.io/github/license/s3r3t0/web-extension)][license]
![GitHub language count](https://img.shields.io/github/languages/count/s3r3t0/web-extension)
![GitHub top language](https://img.shields.io/github/languages/top/s3r3t0/web-extension)

[![OpenSSF Scorecard](https://api.scorecard.dev/projects/github.com/s3r3t0/web-extension/badge)](https://scorecard.dev/viewer/?uri=github.com/s3r3t0/web-extension)

Browser web extension to support easy reporting of cookie issues with the [Security Reporting Tool (SeReTo)][SeReTo].

## Table of Contents

- [SeReTo Helper Web Extension](#sereto-helper-web-extension)
  - [Table of Contents](#table-of-contents)
  - [Usage](#usage)
  - [Getting Started](#getting-started)
    - [Download](#download)
    - [Installing](#installing)
  - [Cookie Lab Test Application](#cookie-lab-test-application)
    - [Prerequisites](#prerequisites)
    - [Host Mapping](#host-mapping)
    - [Quick Start](#quick-start)
    - [Run Modes](#run-modes)
    - [Test and Quality Targets](#test-and-quality-targets)
  - [Wiki](#wiki)
  - [Versioning](#versioning)
  - [License](#license)
  - [Security Policy](#security-policy)
  - [FAQ](#faq)
    - [Does it work with my browser?](#does-it-work-with-my-browser)
    - [Why the extension does not load properly in Flatpak Firefox?](#why-the-extension-does-not-load-properly-in-flatpak-firefox)
  - [Acknowledgements](#acknowledgements)

## Usage

The extension is available in the Mozilla web extension store. Firefox user may got to the [product page](https://addons.mozilla.org/en-US/firefox/addon/sereto-helper/) and click on the `Add to Firefox` button.

If you are using different browser you may continue with the manual installation below. Please, keep in mind that the extension is tested in the Firefox only at the moment.

## Getting Started

These instructions will help you set up the SeReTo helper extension on your local machine for development and testing purposes.

### Download

Clone the repository to your local machine:

```bash
git clone https://github.com/s3r3t0/web-extension
```

Or you can download a source code archive and unpack it.

```bash
curl -L https://api.github.com/repos/s3r3t0/web-extension/tarball/main -o /tmp/sereto_extension
tar -xzvf /tmp/sereto_extension "$HOME/sereto_extension"
```

### Installing

Open the `about:debugging` page in Firefox. Click on "Load Temporary Add-on..." in the "This Firefox" tab. Navigate to the directory where you cloned the repository and select the `manifest.json` file.

The extension is not bundled at the moment. If you need to bundle it, you can run the following command:

```bash
cd src
zip -r -FS ../sereto_extension.zip *
```

## Cookie Lab Test Application

This repository now includes a standards-first Flask testing application to validate cookie handling behavior independently from the extension implementation.

The application provides:

- 18 baseline cookie scenarios (prefixes, SameSite, scope, persistence, path)
- set/clear endpoints for individual and bulk scenario operations
- a browser UI for manual testing
- pytest smoke coverage for scenario metadata and endpoint behavior

### Prerequisites

- Python 3.11+
- [uv](https://docs.astral.sh/uv/)

### Host Mapping

For parent-domain and subdomain scenarios, map the following hosts to localhost:

```text
127.0.0.1 app.localtest.me
127.0.0.1 api.localtest.me
```

### Quick Start

```bash
make bootstrap
make run-https
```

Then open:

- <https://app.localtest.me:8443>
- <https://api.localtest.me:8443>

### Run Modes

- HTTP mode: `make run-http`
- HTTPS mode (recommended for Secure and prefix scenarios): `make run-https`

The HTTPS target uses Flask adhoc certificates, which require the `cryptography` package. This dependency is included in `pyproject.toml` and is installed automatically when using `uv`.

### Test and Quality Targets

- `make test`
- `make test-scenarios`
- `make test-coverage`
- `make test-e2e-install` (one-time browser binaries installation)
- `make test-e2e` (Chromium + Firefox popup smoke tests)
- `make test-e2e-chromium` (CI-friendly default)
- `make test-e2e-firefox`
- `make test-e2e-runtime` (Chromium runtime popup smoke via loaded extension)
- `make lint`
- `make format-check`
- `make precommit`
- `make ci-local`

## Wiki

Project wiki content is under `docs/` and uses native Zensical TOML configuration in `zensical.toml`.

- Serve docs locally: `make docs-serve`
- Build docs: `make docs-build`
- Build docs in strict mode: `make docs-check`
- Publish docs to GitHub Pages: GitHub Actions workflow `Docs to GitHub Pages` (`.github/workflows/deploy-pages.yml`)
- Manual publish trigger: Actions -> `Docs to GitHub Pages` -> `Run workflow`
- Contributor setup and CI maintenance notes: [docs/contributing.md][contributing]

## Versioning

We use [Semantic Versioning][semver] for versioning. For the versions available, see the [tags on this repository][tags] or the full [Changelog].

We keep the major and minor version of the template in sync with [SeReTo].
The latest version of the template is tested with the latest version of SeReTo.

## License

This project is licensed under the [GNU General Public License v3.0][license] - see the [LICENSE][license] file for details.

## Security Policy

Before reporting a security issue, please review our [security policy][security].

## FAQ

### Does it work with my browser?

The extension is designed to work with Firefox.
It may work with other browsers that support WebExtensions API, but it is not guaranteed.
The other browsers are not tested at the moment.

### Why the extension does not load properly in Flatpak Firefox?

Flatpak applications are sandboxed, which can cause issues with loading raw extensions. To resolve this, you may need to load the extension in its bundled form (zip file). For more details see [Installing](#installing) section.

## Acknowledgements

> Created with support of [NN Management Services, s.r.o.][nn]

[SeReTo]: https://github.com/s3r3t0/sereto
[semver]: https://semver.org
[tags]: https://github.com/s3r3t0/web-extension/tags
[license]: https://github.com/s3r3t0/web-extension/blob/main/LICENSE
[Changelog]: https://github.com/s3r3t0/web-extension/blob/main/CHANGELOG.md
[nn]: https://www.nn.cz/kariera/en/nn-digital-hub/
[release]: https://github.com/s3r3t0/web-extension/releases/latest
[security]: https://github.com/s3r3t0/web-extension/blob/main/SECURITY.md
[contributing]: https://github.com/s3r3t0/web-extension/blob/main/docs/contributing.md
