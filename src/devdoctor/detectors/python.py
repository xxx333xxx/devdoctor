from __future__ import annotations
from devdoctor.models import Detector, Finding, ScanContext, Severity
from devdoctor.util import has_file, which, read_text


class PythonDetector(Detector):
    name = "python"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        if not has_file(ctx.root, ["pyproject.toml", "requirements.txt", "setup.py", "Pipfile"]):
            return []
        findings = []
        if not which("python") and not which("python3"):
            findings.append(Finding(self.name, Severity.ERROR, "Python not found", "Python project detected, but no python executable is on PATH.", "Install Python 3.9+ or activate your environment."))
        if (ctx.root / "requirements.txt").exists() and not (ctx.root / ".venv").exists():
            findings.append(Finding(self.name, Severity.INFO, "No local virtualenv", "requirements.txt exists but .venv was not found.", "Run `python -m venv .venv` then install dependencies."))
        pyproject = read_text(ctx.root / "pyproject.toml")
        if "pytest" in pyproject and not (ctx.root / "tests").exists():
            findings.append(Finding(self.name, Severity.WARN, "Pytest configured but no tests directory", "pyproject mentions pytest, but tests/ is missing.", "Add tests/ or remove stale pytest config."))
        return findings
