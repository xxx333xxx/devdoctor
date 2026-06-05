# OpenAI OSS Application Notes

Use this as a working draft for the Codex for Open Source application.

## Project

DevDoctor

## Repository

https://github.com/xxx333xxx/devdoctor

## Short pitch

DevDoctor helps OSS maintainers prevent contributor onboarding failures by checking whether README setup steps, env files, runtimes, Docker ports, and repo metadata still match reality.

## Why this project qualifies

Open-source projects often have good production CI but fragile local onboarding. A new contributor may follow the README and still fail because `.env` setup is missing, runtime versions are unclear, Docker ports conflict, or the documented command no longer exists.

DevDoctor targets that gap directly. It treats README setup instructions and local development requirements as testable infrastructure. The goal is to become "CI for README files and local development setup."

## How Codex would help

- Build additional detectors for README command drift, `.env.example` key drift, and framework-specific setup failures.
- Generate realistic fixture repositories for tests.
- Review pull requests for false positives and unsafe checks.
- Improve documentation, release notes, and examples.
- Add CI/SARIF integration so maintainers can run DevDoctor on pull requests.

## Current signals to mention

- Public GitHub repository: https://github.com/xxx333xxx/devdoctor
- Version 0.2.1 includes multiple detectors, CI-friendly CLI controls, and PyPI-ready packaging as `devdoctor-cli`.
- Reddit feedback route started in r/devops weekly self-promotion thread.
- Roadmap for 0.3.0 focuses on README command drift, environment drift, and CI integration.

## Application answer draft

DevDoctor helps OSS maintainers prevent contributor onboarding failures by checking whether README setup steps, env files, runtimes, Docker ports, and repo metadata still match reality. It targets a common OSS problem: CI can be green while new contributors cannot run the project locally. I am the primary maintainer and plan to use Codex for checks, tests, PR review, docs, and release automation.
