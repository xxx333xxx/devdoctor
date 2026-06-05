from __future__ import annotations
import re
from devdoctor.models import Detector, Finding, ScanContext, Severity
from devdoctor.util import read_text, which


class DockerDetector(Detector):
    name = "docker"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        files = [ctx.root / "docker-compose.yml", ctx.root / "docker-compose.yaml", ctx.root / "compose.yml"]
        compose = next((p for p in files if p.exists()), None)
        findings = []
        if compose and not which("docker"):
            findings.append(Finding(self.name, Severity.ERROR, "Docker not found", f"{compose.name} exists but docker is not on PATH.", "Install Docker or document a non-Docker setup path."))
        if compose:
            text = read_text(compose)
            ports = re.findall(r"['\"]?(\d{2,5}):(\d{2,5})['\"]?", text)
            seen = set()
            dupes = []
            for host, _container in ports:
                if host in seen:
                    dupes.append(host)
                seen.add(host)
            if dupes:
                findings.append(Finding(self.name, Severity.WARN, "Duplicate host ports in compose", ", ".join(sorted(set(dupes))), "Change one host port or split services into profiles."))
        return findings
