# Contributing

Thanks for helping improve DevDoctor.

The most useful contributions are real setup failures that made a repository hard to run locally.

## Good issue reports

Please include:

- the framework or stack
- the README command that failed
- the file that contained the real command or missing setup requirement
- what DevDoctor should detect
- what fix message would have helped

Example:

```text
README says npm start, but package.json only has npm run dev.
DevDoctor should warn that the README command does not exist.
Suggested fix: update README or add the missing script.
```

## Development

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e ".[dev]"
pytest
```

## Design principles

- Prefer checks that are easy to explain.
- Prefer warnings with practical fixes over clever inference.
- Avoid destructive behavior.
- Keep false positives low.
- Treat README setup docs as part of the developer experience, not an afterthought.
