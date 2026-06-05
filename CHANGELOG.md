# Changelog

All notable changes to DevDoctor are documented here.

## 0.2.0 - 2026-06-05

### Added

- Secret scanning for committed `.env` files, token-like values, and private key blocks.
- `devdoctor list-checks` for showing enabled detectors.
- `--min-severity` and `--fail-on` flags for CI-friendly scans.
- GitHub Actions, README, Docker, Python, Node, env, git, and secrets detector coverage.

### Changed

- Improved CLI output so warnings and errors are easier to use in local onboarding checks.

## 0.1.0 - 2026-06-05

### Added

- Initial DevDoctor CLI.
- Local repository scan command.
- README command extraction and optional README command verification.
- Basic tests for core scan behavior.
