# DevDoctor

DevDoctor is a small open-source CLI that diagnoses common local development setup problems before a new contributor loses an afternoon.

It is intentionally boring: it checks the repo, README, package managers, `.env`, Docker Compose, Python/Node setup and GitHub Actions, then prints fixes.

## Why

Modern projects often have good production CI but bad local onboarding. DevDoctor treats the README and local setup as testable infrastructure.

## Install

```bash
pip install -e .
```

For development:

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
```

## Usage

```bash
devdoctor scan .
devdoctor scan . --json
devdoctor verify-readme .
devdoctor verify-readme . --run
```

## What it checks

- missing `.env` when `.env.example` exists
- multiple Node lockfiles
- missing Node/Python executables
- duplicate Docker Compose host ports
- README without copy-pasteable commands
- risky README quickstart commands
- missing or weak GitHub Actions workflows
- missing `.gitignore`

## Philosophy

DevDoctor is not a replacement for Dev Containers, Docker, Nix, mise, asdf, or CI. It is the fast diagnostic layer that explains why a repo fails to start locally.

## Roadmap

- plugin API
- SARIF output for GitHub code scanning
- README command sandbox using containers
- first-class checks for Next.js, Django, FastAPI, Rails and Go
- `devdoctor doctor` automatic safe fixes

## Test

```bash
pytest
```

## Status

This is an early MVP. The scanner is intentionally conservative and focuses on checks that are easy to explain and safe to run locally.

## License

MIT
