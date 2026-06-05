# GitHub Actions

DevDoctor can run in CI as a lightweight onboarding check.

Create `.github/workflows/devdoctor.yml`:

```yaml
name: DevDoctor

on:
  pull_request:
    paths:
      - "README.md"
      - "docs/**"
      - "package.json"
      - "pyproject.toml"
      - "docker-compose*.yml"
      - ".github/workflows/**"
      - ".env.example"
  push:
    branches: [main]

jobs:
  scan:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: "3.11"
      - run: pip install git+https://github.com/xxx333xxx/devdoctor.git
      - run: devdoctor scan . --min-severity warn --fail-on error
```

This configuration is intentionally conservative: warnings are visible, but only errors fail the job.

For stricter repositories, use:

```bash
devdoctor scan . --min-severity warn --fail-on warn
```
