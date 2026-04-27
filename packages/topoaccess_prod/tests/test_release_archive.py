from pathlib import Path

from topoaccess_prod.release.release_archive import build_release_archive


def test_release_archive_builds(tmp_path: Path):
    pkg = tmp_path / "pkg"
    (pkg / "topoaccess_prod").mkdir(parents=True)
    (pkg / "topoaccess_prod" / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "README.md").write_text("readme", encoding="utf-8")
    release = tmp_path / "release"
    release.mkdir()
    (release / "release_manifest.json").write_text("{}", encoding="utf-8")
    row = build_release_archive(str(pkg), str(release), str(tmp_path / "out.jsonl"), str(tmp_path / "report.md"))
    assert row["archive_exists"] is True

