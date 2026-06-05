from __future__ import annotations
import argparse, json, sys
from devdoctor.scanner import DETECTORS, scan
from devdoctor.report import render_text, render_json
from devdoctor.readme_verify import verify_readme
from devdoctor.models import Severity


SEVERITY_ORDER = {Severity.INFO: 0, Severity.WARN: 1, Severity.ERROR: 2}


def filter_findings(findings, minimum: str):
    min_severity = Severity(minimum)
    return [f for f in findings if SEVERITY_ORDER[f.severity] >= SEVERITY_ORDER[min_severity]]


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="devdoctor", description="Diagnose local dev environment and README setup issues.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="Scan a repository")
    s.add_argument("path", nargs="?", default=".")
    s.add_argument("--json", action="store_true")
    s.add_argument("--min-severity", choices=[s.value for s in Severity], default=Severity.INFO.value, help="Only show findings at or above this severity")
    s.add_argument("--fail-on", choices=[s.value for s in Severity], default=Severity.ERROR.value, help="Exit 1 when this severity or higher is found")
    v = sub.add_parser("verify-readme", help="Extract and optionally run README commands")
    v.add_argument("path", nargs="?", default=".")
    v.add_argument("--run", action="store_true", help="Run safe commands instead of dry-run")
    sub.add_parser("list-checks", help="List enabled detectors")
    args = parser.parse_args(argv)

    if args.cmd == "scan":
        findings = scan(args.path)
        shown = filter_findings(findings, args.min_severity)
        print(render_json(shown) if args.json else render_text(shown))
        fail_severity = Severity(args.fail_on)
        return 1 if any(SEVERITY_ORDER[f.severity] >= SEVERITY_ORDER[fail_severity] for f in findings) else 0
    if args.cmd == "verify-readme":
        print(json.dumps(verify_readme(args.path, dry_run=not args.run), indent=2))
        return 0
    if args.cmd == "list-checks":
        print("\n".join(detector.name for detector in DETECTORS))
        return 0
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
