from __future__ import annotations
import shlex
from pathlib import Path
from devdoctor.util import extract_commands, read_text, run

ALLOW_PREFIXES = ("npm ", "pnpm ", "yarn ", "pip ", "python ", "pytest", "make ", "go ", "cargo ")
DENY = ("sudo", "rm ", "curl", "wget", "docker")


def verify_readme(root: str | Path, max_commands: int = 6, dry_run: bool = True) -> list[dict]:
    root = Path(root).resolve()
    commands = extract_commands(read_text(root / "README.md"))[:max_commands]
    results = []
    for cmd in commands:
        safe = cmd.startswith(ALLOW_PREFIXES) and not any(cmd.startswith(x) or f" {x}" in cmd for x in DENY)
        if dry_run or not safe:
            results.append({"command": cmd, "status": "skipped", "reason": "dry-run" if dry_run else "unsafe"})
        else:
            code, output = run(shlex.split(cmd), root, timeout=20)
            results.append({"command": cmd, "status": "pass" if code == 0 else "fail", "exit_code": code, "output": output[-1000:]})
    return results
