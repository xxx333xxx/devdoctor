from __future__ import annotations
import re
from devdoctor.models import Detector, Finding, ScanContext, Severity
from devdoctor.util import extract_commands


DANGEROUS = ("rm -rf /", "sudo rm", "mkfs", ":(){", "curl ", "wget ")


class ReadmeDetector(Detector):
    name = "readme"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        findings = []
        if not ctx.readme_text:
            return [Finding(self.name, Severity.WARN, "Missing README", "No README.md was found.", "Add a README with install, run and test steps.")]
        text = ctx.readme_text.lower()
        for heading in ("install", "usage", "test"):
            if heading not in text:
                findings.append(Finding(self.name, Severity.INFO, f"README missing {heading} section", f"Could not find `{heading}` in README.", f"Add a `{heading}` section."))
        commands = extract_commands(ctx.readme_text)
        if not commands:
            findings.append(Finding(self.name, Severity.WARN, "README has no runnable setup commands", "No shell commands were detected in fenced code blocks.", "Add copy-pasteable setup commands."))
        risky = [c for c in commands if any(x in c for x in DANGEROUS)]
        if risky:
            findings.append(Finding(self.name, Severity.WARN, "README contains risky setup commands", "; ".join(risky[:3]), "Avoid remote shell pipes and destructive commands in quickstarts."))
        return findings
