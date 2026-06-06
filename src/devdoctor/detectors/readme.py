from __future__ import annotations
import json
import re
from devdoctor.models import Detector, Finding, ScanContext, Severity
from devdoctor.util import extract_commands, read_text


DANGEROUS = ("rm -rf /", "sudo rm", "mkfs", ":(){", "curl ", "wget ")

NPM_SCRIPT_COMMANDS = {
    "start",
    "stop",
    "restart",
    "test",
}


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
        findings.extend(_detect_package_script_drift(ctx, commands))
        return findings


def _detect_package_script_drift(ctx: ScanContext, commands: list[str]) -> list[Finding]:
    pkg = ctx.root / "package.json"
    if not pkg.exists():
        return []
    try:
        data = json.loads(read_text(pkg))
    except json.JSONDecodeError:
        return []
    scripts = data.get("scripts")
    if not isinstance(scripts, dict):
        return []
    script_names = {str(name) for name in scripts}
    findings: list[Finding] = []
    for command in commands:
        expected = _referenced_package_script(command)
        if not expected or expected in script_names:
            continue
        available = ", ".join(f"`npm run {name}`" for name in sorted(script_names)[:5]) or "no package scripts"
        findings.append(
            Finding(
                ReadmeDetector.name,
                Severity.ERROR,
                "README setup command does not exist",
                f"README uses `{command}`, but package.json does not define script `{expected}`. Available: {available}.",
                f"Update the README command or add a `{expected}` script to package.json.",
                evidence=[command, f"package.json scripts: {', '.join(sorted(script_names)) or '(none)'}"],
            )
        )
    return findings


def _referenced_package_script(command: str) -> str | None:
    normalized = re.sub(r"\s+", " ", command.strip())
    match = re.match(r"^(npm|pnpm|bun)\s+run\s+([A-Za-z0-9:_./-]+)\b", normalized)
    if match:
        return match.group(2)
    match = re.match(r"^(npm|pnpm|bun)\s+([A-Za-z0-9:_./-]+)\b", normalized)
    if match and match.group(2) in NPM_SCRIPT_COMMANDS:
        return match.group(2)
    match = re.match(r"^yarn\s+([A-Za-z0-9:_./-]+)\b", normalized)
    if match and match.group(1) not in {"add", "install", "remove", "upgrade", "dlx", "set", "config"}:
        return match.group(1)
    return None
