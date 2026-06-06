# Changelog

All notable changes to DevDoctor are documented here.

## 0.3.0 - 2026-06-06

### Added

- README/package script drift detection for Node projects.
- DevDoctor now reports an error when README setup commands reference package scripts that do not exist, such as `npm start` when `package.json` only defines `npm run dev`.
- Tests covering missing and valid README package script references.

## 0.2.1 - 2026-06-05

### Changed

- Renamed the PyPI distribution to `devdoctor-cli` because the `devdoctor` package name is already occupied on PyPI.
- Kept the installed console command as `devdoctor`.
- Added PyPI install instructions to the README.

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
