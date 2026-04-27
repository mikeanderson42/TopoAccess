from pathlib import Path

from topoaccess_prod.release.license_finalize import finalize_license


def test_license_finalize_writes_apache(tmp_path: Path):
    pkg = tmp_path / "pkg"; (pkg / "docs").mkdir(parents=True)
    (pkg / "pyproject.toml").write_text('[project]\nauthors = [{name = "Mike / project owner"}]\n', encoding="utf-8")
    (pkg / "README.md").write_text("# X\n", encoding="utf-8")
    row = finalize_license(str(pkg), "apache-2.0", "Mike", str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert row["license_confirmed"] is True
    assert (pkg / "LICENSE").exists()

