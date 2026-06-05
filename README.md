# DevDoctor

DevDoctor is a small open-source CLI that diagnoses common local development setup problems before a new contributor loses an afternoon.

It is intentionally boring: it checks the repo, README, package managers, `.env`, Docker Compose, Python/Node setup and GitHub Actions, then prints fixes.

## Why

Modern projects often have good production CI but bad local onboarding. DevDoctor treats the README and local setup as testable infrastructure.

## Install

From PyPI:

```bash
pipx install devdoctor-cli
```

From GitHub:

```bash
pipx install git+https://github.com/xxx333xxx/devdoctor.git
```

From a local checkout:

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
devdoctor scan . --min-severity warn --fail-on warn
devdoctor list-checks
devdoctor verify-readme .
devdoctor verify-readme . --run
```

## GitHub Actions

DevDoctor can run on pull requests when setup-related files change:

```yaml
- run: pip install git+https://github.com/xxx333xxx/devdoctor.git
- run: devdoctor scan . --min-severity warn --fail-on error
```

See [docs/github-actions.md](docs/github-actions.md) for a full workflow.

## What it checks

- missing `.env` when `.env.example` exists
- committed secret files or token-like values
- multiple Node lockfiles
- missing Node/Python executables
- duplicate Docker Compose host ports
- README without copy-pasteable commands
- risky README quickstart commands
- missing or weak GitHub Actions workflows
- missing `.gitignore`

## Example output

DevDoctor is meant to catch the small setup failures that make a repo feel abandoned before a contributor reaches the real code.

```text
DevDoctor found 3 issue(s): 1 error, 2 warn, 0 info

ERROR [readme] README setup command does not exist
   README uses `npm start`, but package.json only defines `npm run dev`.
   Fix: Update the README command or add the missing package script.

WARN [env] Missing .env
   .env.example exists, but .env is missing.
   Fix: cp .env.example .env

WARN [docker] Duplicate Docker Compose host port
   Port 5432 is used by more than one service.
   Fix: Change one host port or stop the conflicting service.
```

The goal is simple: if a README claims a repo can be started locally, that path should be cheap to check.

## Philosophy

DevDoctor is not a replacement for Dev Containers, Docker, Nix, mise, asdf, or CI. It is the fast diagnostic layer that explains why a repo fails to start locally.

## Roadmap

See [ROADMAP.md](ROADMAP.md) for the 0.3.0 plan.

Near-term focus:

- README command verifier that compares documented commands with package manager scripts
- `.env.example` key drift checks
- GitHub Actions mode for setup-doc checks on pull requests
- SARIF output for GitHub code scanning
- README command sandbox using containers

## What's new in 0.2.0

- secret scanning for `.env`, token-like values and private key blocks
- `devdoctor list-checks` to show enabled detectors
- `--min-severity` and `--fail-on` controls for CI-friendly scans
- PyPI distribution name is `devdoctor-cli`; the installed command remains `devdoctor`

See [CHANGELOG.md](CHANGELOG.md) for release history.

## Test

```bash
pytest
```

## Status

This is an early MVP. The scanner is intentionally conservative and focuses on checks that are easy to explain and safe to run locally.

Feedback is especially useful if you have a real "README said one thing, local setup needed another" failure story. Open an issue with the repo, framework, and the command that failed.

## License

MIT
