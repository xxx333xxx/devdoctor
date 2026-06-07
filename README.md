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

Try the intentionally broken demo fixture:

```bash
devdoctor scan examples/broken-node
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
- README package script drift, such as `npm start` missing from `package.json`
- missing Node/Python executables
- duplicate Docker Compose host ports
- README without copy-pasteable commands
- risky README quickstart commands
- missing or weak GitHub Actions workflows
- missing `.gitignore`

## Example output

DevDoctor is meant to catch the small setup failures that make a repo feel abandoned before a contributor reaches the real code.

```text
DevDoctor found 9 issue(s): 1 error, 4 warn, 4 info

WARN [env] Missing .env
   Found .env.example, but no .env file.
   Fix: Copy `.env.example` to `.env` and fill required values.

WARN [node] Multiple package manager lockfiles
   package-lock.json, yarn.lock
   Fix: Keep exactly one lockfile to avoid dependency drift.

ERROR [readme] README setup command does not exist
   README uses `npm start`, but package.json does not define script `start`. Available: `npm run dev`.
   Evidence: npm start, package.json scripts: dev
   Fix: Update the README command or add a `start` script to package.json.
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

## What's new in 0.3.0

- README/package script drift detection for Node projects
- detects stale setup commands like `npm start` when only `npm run dev` exists
- keeps the PyPI distribution name `devdoctor-cli`; the installed command remains `devdoctor`

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
