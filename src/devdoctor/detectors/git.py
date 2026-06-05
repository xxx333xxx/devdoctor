from __future__ import annotations
from devdoctor.models import Detector, Finding, ScanContext, Severity


class GitDetector(Detector):
    name = "git"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        findings = []
        if not (ctx.root / ".git").exists():
            findings.append(Finding(self.name, Severity.INFO, "Not a Git repository", "No .git directory was found.", "Run `git init` if this is meant to be a repo."))
        if not (ctx.root / ".gitignore").exists():
            findings.append(Finding(self.name, Severity.WARN, "Missing .gitignore", "Common generated files may be committed accidentally.", "Add a .gitignore for your stack."))
        return findings
