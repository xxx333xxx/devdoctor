from __future__ import annotations
from devdoctor.models import Detector, Finding, ScanContext, Severity
from devdoctor.util import read_text


class GitHubActionsDetector(Detector):
    name = "github-actions"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        wf_dir = ctx.root / ".github" / "workflows"
        if not wf_dir.exists():
            return [Finding(self.name, Severity.INFO, "No GitHub Actions workflow", "No .github/workflows directory was found.", "Add CI to run tests and `devdoctor scan` on pull requests.")]
        findings = []
        for wf in wf_dir.glob("*.y*ml"):
            txt = read_text(wf)
            if "pull_request" not in txt and "push" not in txt:
                findings.append(Finding(self.name, Severity.WARN, "Workflow may not run on PRs/pushes", wf.name, "Add `on: [push, pull_request]` or equivalent."))
            if "actions/checkout" not in txt:
                findings.append(Finding(self.name, Severity.WARN, "Workflow missing checkout", wf.name, "Most workflows need actions/checkout before running project commands."))
        return findings
