from __future__ import annotations
import json
from devdoctor.models import Detector, Finding, ScanContext, Severity
from devdoctor.util import read_text, which


class NodeDetector(Detector):
    name = "node"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        findings = []
        pkg = ctx.root / "package.json"
        if not pkg.exists():
            return findings
        try:
            data = json.loads(read_text(pkg))
        except json.JSONDecodeError as exc:
            return [Finding(self.name, Severity.ERROR, "Invalid package.json", str(exc), "Fix JSON syntax.")]
        if not which("node"):
            findings.append(Finding(self.name, Severity.ERROR, "Node.js not found", "package.json exists but node is not on PATH.", "Install Node.js or use fnm/nvm/asdf."))
        locks = [n for n in ("package-lock.json", "pnpm-lock.yaml", "yarn.lock", "bun.lockb") if (ctx.root / n).exists()]
        if len(locks) > 1:
            findings.append(Finding(self.name, Severity.WARN, "Multiple package manager lockfiles", ", ".join(locks), "Keep exactly one lockfile to avoid dependency drift."))
        scripts = data.get("scripts", {})
        if not scripts:
            findings.append(Finding(self.name, Severity.INFO, "No npm scripts", "package.json has no scripts section.", "Add setup/test/dev scripts for new contributors."))
        if scripts and "test" not in scripts:
            findings.append(Finding(self.name, Severity.WARN, "No test script", "No `test` script was found.", "Add `npm test` or document why tests are unavailable."))
        return findings
