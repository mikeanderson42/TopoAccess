from pathlib import Path

from topoaccess_prod.release.publish_readiness import publish_readiness


def test_publish_readiness_local_release(tmp_path: Path):
    package = tmp_path / "pkg"; package.mkdir()
    (package / "LICENSE.md").write_text("No standalone product license.\n", encoding="utf-8")
    release = tmp_path / "rel"; release.mkdir()
    (release / "release_manifest.json").write_text("{}", encoding="utf-8")
    row = publish_readiness(str(package), str(release), "missing-branch", str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert row["local_release_ready"] is True
    assert row["public_publish_ready"] is False

