# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.0] - 2025-11-05

### Added

- Provide multiple cookie output based selected configuration weaknesses
- add locators to output

### Changed

- Filter cookies that do not belong to the active tab domain

## [0.0.3] - 2025-11-03

### Changed

- Use `const` and `let` for variables, use template strings
- Use parent domain for cookies instead of full hostname

## [0.0.2] - 2025-10-22

### Changed

- Match cookies by domain instead of URL
- Use clipboard API for `copyCookies` function

### Fixed

- Use `chrome` variable instead of `browser` when applicable
- Handle `unspecified` value for cookies

## [0.0.1] - 2025-06-18

Initial version

[Unreleased]: https://github.com/s3r3t0/web-extension/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/s3r3t0/web-extension/compare/v0.0.3...v0.1.0
[0.0.3]: https://github.com/s3r3t0/web-extension/compare/v0.0.2...v0.0.3
[0.0.2]: https://github.com/s3r3t0/web-extension/compare/v0.0.1...v0.0.2
[0.0.1]: https://github.com/s3r3t0/web-extension/releases/tag/v0.0.1
