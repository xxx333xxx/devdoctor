from __future__ import annotations
import re
from devdoctor.models import Detector, Finding, ScanContext, Severity
from devdoctor.util import read_text


class EnvDetector(Detector):
    name = "env"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        findings = []
        sample_files = [p for p in ctx.root.iterdir() if p.name in (".env.example", ".env.sample", "example.env")]
        env_file = ctx.root / ".env"
        if sample_files and not env_file.exists():
            findings.append(Finding(self.name, Severity.WARN, "Missing .env", f"Found {sample_files[0].name}, but no .env file.", f"Copy `{sample_files[0].name}` to `.env` and fill required values."))
        text = "\n".join(read_text(p) for p in sample_files)
        required = re.findall(r"^([A-Z][A-Z0-9_]+)=", text, re.M)
        if required and env_file.exists():
            current = read_text(env_file)
            missing = [k for k in required if not re.search(rf"^{re.escape(k)}=", current, re.M)]
            if missing:
                findings.append(Finding(self.name, Severity.ERROR, "Missing environment variables", ", ".join(missing), "Add the missing keys to `.env`.", missing))
        return findings
