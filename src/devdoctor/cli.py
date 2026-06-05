from __future__ import annotations
import argparse, json, sys
from devdoctor.scanner import scan
from devdoctor.report import render_text, render_json
from devdoctor.readme_verify import verify_readme
from devdoctor.models import Severity


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="devdoctor", description="Diagnose local dev environment and README setup issues.")
    sub = parser.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("scan", help="Scan a repository")
    s.add_argument("path", nargs="?", default=".")
    s.add_argument("--json", action="store_true")
    v = sub.add_parser("verify-readme", help="Extract and optionally run README commands")
    v.add_argument("path", nargs="?", default=".")
    v.add_argument("--run", action="store_true", help="Run safe commands instead of dry-run")
    args = parser.parse_args(argv)

    if args.cmd == "scan":
        findings = scan(args.path)
        print(render_json(findings) if args.json else render_text(findings))
        return 1 if any(f.severity == Severity.ERROR for f in findings) else 0
    if args.cmd == "verify-readme":
        print(json.dumps(verify_readme(args.path, dry_run=not args.run), indent=2))
        return 0
    return 2

if __name__ == "__main__":
    raise SystemExit(main())
