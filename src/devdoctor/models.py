from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import List, Optional


class Severity(str, Enum):
    INFO = "info"
    WARN = "warn"
    ERROR = "error"


@dataclass
class Finding:
    detector: str
    severity: Severity
    title: str
    message: str
    fix: Optional[str] = None
    evidence: List[str] = field(default_factory=list)


@dataclass
class ScanContext:
    root: Path
    readme_text: str = ""


class Detector:
    name = "base"

    def detect(self, ctx: ScanContext) -> list[Finding]:
        raise NotImplementedError
