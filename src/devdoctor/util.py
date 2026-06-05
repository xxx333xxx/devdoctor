from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path
from typing import Iterable


def read_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return path.read_text(errors="ignore")
    except FileNotFoundError:
        return ""


def has_file(root: Path, names: Iterable[str]) -> bool:
    return any((root / n).exists() for n in names)


def which(cmd: str) -> str | None:
    return shutil.which(cmd)


def run(cmd: list[str], cwd: Path, timeout: int = 10) -> tuple[int, str]:
    try:
        proc = subprocess.run(cmd, cwd=str(cwd), text=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, timeout=timeout)
        return proc.returncode, proc.stdout.strip()
    except Exception as exc:  # pragma: no cover
        return 127, str(exc)


def extract_code_blocks(markdown: str) -> list[str]:
    blocks = []
    for match in re.finditer(r"```(?:bash|sh|shell|console)?\n(.*?)```", markdown, re.S | re.I):
        block = match.group(1).strip()
        if block:
            blocks.append(block)
    return blocks


def extract_commands(markdown: str) -> list[str]:
    commands: list[str] = []
    for block in extract_code_blocks(markdown):
        for line in block.splitlines():
            line = line.strip()
            if not line or line.startswith("#"):
                continue
            line = re.sub(r"^[$>]\s*", "", line)
            if re.match(r"^(npm|pnpm|yarn|pip|poetry|uv|python|pytest|docker|docker compose|make|go|cargo)\b", line):
                commands.append(line)
    return commands
