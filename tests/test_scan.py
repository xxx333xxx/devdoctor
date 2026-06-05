from pathlib import Path
from devdoctor.scanner import scan
from devdoctor.readme_verify import verify_readme


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
