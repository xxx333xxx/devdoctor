# Roadmap

DevDoctor's north star is simple:

> CI for README files and local development setup.

The project focuses on a common open-source failure mode: production CI is green, but a new contributor cannot run the repository from the README.

## 0.3.0 Focus

### README command drift

- Detect README commands that reference missing package manager scripts.
- Example: README says `npm start`, but `package.json` only has `npm run dev`.
- Start with Node projects, then extend to Python, Go, Rails, and common framework CLIs.

### Environment drift

- Compare `.env.example` with obvious environment keys referenced in source files.
- Warn when `.env.example` exists but required keys appear undocumented.
- Keep the detector conservative to avoid noisy false positives.

### CI integration

- Add a documented GitHub Actions recipe.
- Support output modes that are easy to consume in CI.
- Add SARIF output for code scanning integrations.

### Demo coverage

- Add fixture repositories that intentionally fail in realistic ways.
- Use those fixtures in tests and documentation.

## Later

- Plugin API for project-specific checks.
- Container-backed README command sandbox.
- `devdoctor doctor` for safe automatic fixes.
- Framework-specific checks for Next.js, Django, FastAPI, Rails, Go, and common monorepo layouts.

## Non-goals

- DevDoctor is not a replacement for tests, Docker, Dev Containers, Nix, mise, asdf, or CI.
- DevDoctor should not run destructive commands.
- DevDoctor should not become a giant vague checklist. Every check should explain a real setup failure and a practical fix.
