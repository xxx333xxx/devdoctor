from pathlib import Path
from devdoctor.scanner import scan
from devdoctor.readme_verify import verify_readme
from devdoctor.cli import main


def test_detects_missing_env(tmp_path: Path):
    (tmp_path / ".env.example").write_text("DATABASE_URL=\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# X\n```bash\npytest\n```", encoding="utf-8")
    findings = scan(tmp_path)
    assert any(f.title == "Missing .env" for f in findings)


def test_detects_multiple_node_locks(tmp_path: Path):
    (tmp_path / "package.json").write_text('{"scripts":{"dev":"vite"}}', encoding="utf-8")
    (tmp_path / "package-lock.json").write_text("{}", encoding="utf-8")
    (tmp_path / "yarn.lock").write_text("", encoding="utf-8")
    (tmp_path / "README.md").write_text("# X\n```bash\nnpm install\n```", encoding="utf-8")
    findings = scan(tmp_path)
    assert any("Multiple package manager" in f.title for f in findings)


def test_verify_readme_extracts_commands(tmp_path: Path):
    (tmp_path / "README.md").write_text("```bash\n$ pip install -e .\npytest\n```", encoding="utf-8")
    results = verify_readme(tmp_path)
    assert [r["command"] for r in results] == ["pip install -e .", "pytest"]


def test_detects_committed_env_file(tmp_path: Path):
    (tmp_path / ".env").write_text("API_TOKEN=super-secret-value\n", encoding="utf-8")
    (tmp_path / "README.md").write_text("# X\n```bash\npytest\n```", encoding="utf-8")
    findings = scan(tmp_path)
    assert any(f.detector == "secrets" and f.title == "Possible secret file committed" for f in findings)


def test_min_severity_can_hide_info_findings(tmp_path: Path, capsys):
    (tmp_path / "README.md").write_text("# X\n```bash\npytest\n```", encoding="utf-8")
    code = main(["scan", str(tmp_path), "--min-severity", "warn", "--fail-on", "error"])
    assert code == 0
    assert "Not a Git repository" not in capsys.readouterr().out


def test_list_checks(capsys):
    assert main(["list-checks"]) == 0
    out = capsys.readouterr().out
    assert "secrets" in out
