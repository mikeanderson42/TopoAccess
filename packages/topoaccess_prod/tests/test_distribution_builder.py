from pathlib import Path

from topoaccess_prod.release.distribution_builder import fallback_archive


def test_fallback_archive_contains_package(tmp_path: Path):
    pkg = tmp_path / "pkg"
    (pkg / "topoaccess_prod").mkdir(parents=True)
    (pkg / "topoaccess_prod" / "__init__.py").write_text("", encoding="utf-8")
    (pkg / "README.md").write_text("readme", encoding="utf-8")
    archive = fallback_archive(pkg, tmp_path / "dist")
    assert archive.exists()
    assert archive.suffix == ".gz"

