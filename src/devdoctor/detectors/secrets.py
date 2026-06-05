from __future__ import annotations

import re

from devdoctor.models import Detector, Finding, ScanContext, Severity
from devdoctor.util import iter_repo_files, read_text


SECRET_FILE_NAMES = {".env", ".npmrc", ".pypirc", "id_rsa", "id_ed25519"}
SECRET_PATTERNS = [
    ("AWS access key", re.compile(r"\bAKIA[0-9A-Z]{16}\b")),
    ("GitHub token", re.compile(r"\bgh[pousr]_[A-Za-z0-9_]{20,}\b")),
    ("OpenAI API key", re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b")),
    ("Private key block", re.compile(r"-----BEGIN (?:RSA |OPENSSH |EC |DSA )?PRIVATE KEY-----")),
    ("Likely secret assignment", re.compile(r"(?i)\b(api[_-]?key|secret|token|password)\b\s*=\s*['\"]?[^'\"\n]{12,}")),
]


class SecretsDetector(Detector):
    name = "secrets"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        findings: list[Finding] = []
        for path in iter_repo_files(ctx.root):
            rel = path.relative_to(ctx.root).as_posix()
            if path.name in SECRET_FILE_NAMES and ".example" not in path.name and ".sample" not in path.name:
                findings.append(
                    Finding(
                        self.name,
                        Severity.ERROR,
                        "Possible secret file committed",
                        f"`{rel}` looks like a local credential/config file.",
                        "Remove it from Git, rotate exposed values, and keep only a sample file.",
                        [rel],
                    )
                )
                continue
            text = read_text(path)
            for label, pattern in SECRET_PATTERNS:
                if pattern.search(text):
                    findings.append(
                        Finding(
                            self.name,
                            Severity.ERROR,
                            f"Possible {label} committed",
                            f"`{rel}` contains text matching a secret pattern.",
                            "Remove the secret, rotate it, and add a safe placeholder instead.",
                            [rel],
                        )
                    )
                    break
        return findings
