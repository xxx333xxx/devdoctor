from __future__ import annotations
import json
from collections import Counter
from devdoctor.models import Finding, Severity


def render_text(findings: list[Finding]) -> str:
    if not findings:
        return "OK: No issues found."
    counts = Counter(f.severity for f in findings)
    lines = [f"DevDoctor found {len(findings)} issue(s): {counts[Severity.ERROR]} error, {counts[Severity.WARN]} warn, {counts[Severity.INFO]} info", ""]
    icon = {Severity.ERROR: "ERROR", Severity.WARN: "WARN", Severity.INFO: "INFO"}
    for f in findings:
        lines.append(f"{icon[f.severity]} [{f.detector}] {f.title}")
        lines.append(f"   {f.message}")
        if f.evidence:
            lines.append(f"   Evidence: {', '.join(f.evidence[:5])}")
        if f.fix:
            lines.append(f"   Fix: {f.fix}")
        lines.append("")
    return "\n".join(lines).rstrip()


def render_json(findings: list[Finding]) -> str:
    return json.dumps([f.__dict__ | {"severity": f.severity.value} for f in findings], indent=2)
