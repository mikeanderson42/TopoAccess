from pathlib import Path

from topoaccess_prod.release.owner_metadata import update_owner_metadata


def test_owner_metadata_updates_files(tmp_path: Path):
    pkg = tmp_path / "pkg"
    pkg.mkdir()
    (pkg / "pyproject.toml").write_text('[project]\nauthors = [{name = "Mike"}]\n', encoding="utf-8")
    (pkg / "README.md").write_text("# Package\nMike / project owner\n", encoding="utf-8")
    row = update_owner_metadata(str(pkg), "Michael A. Anderson", "MikeAnderson42@gmail.com", str(tmp_path / "out.jsonl"), str(tmp_path / "report.md"))
    assert row["metadata_owner"] == "Michael A. Anderson <MikeAnderson42@gmail.com>"
    assert "Michael A. Anderson" in (pkg / "AUTHORS.md").read_text(encoding="utf-8")

