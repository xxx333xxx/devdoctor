from __future__ import annotations
from pathlib import Path
from devdoctor.models import Finding, ScanContext
from devdoctor.util import read_text
from devdoctor.detectors.git import GitDetector
from devdoctor.detectors.env import EnvDetector
from devdoctor.detectors.node import NodeDetector
from devdoctor.detectors.python import PythonDetector
from devdoctor.detectors.docker import DockerDetector
from devdoctor.detectors.readme import ReadmeDetector
from devdoctor.detectors.github_actions import GitHubActionsDetector
from devdoctor.detectors.secrets import SecretsDetector

DETECTORS = [
    GitDetector(),
    EnvDetector(),
    SecretsDetector(),
    NodeDetector(),
    PythonDetector(),
    DockerDetector(),
    ReadmeDetector(),
    GitHubActionsDetector(),
]


def scan(root: str | Path) -> list[Finding]:
    path = Path(root).resolve()
    ctx = ScanContext(path, read_text(path / "README.md"))
    findings: list[Finding] = []
    for detector in DETECTORS:
        findings.extend(detector.detect(ctx))
    return findings
