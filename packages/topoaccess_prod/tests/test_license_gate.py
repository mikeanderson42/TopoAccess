from pathlib import Path

from topoaccess_prod.harness.license_gate import run_license_gate


def test_license_gate_blocks_unconfirmed_public_release(tmp_path: Path):
    package = tmp_path / "pkg"
    package.mkdir()
    (package / "LICENSE.md").write_text("Mike must choose the intended license.\n", encoding="utf-8")
    (package / "AUTHORS.md").write_text("Mike\n", encoding="utf-8")
    (package / "CREDITS.md").write_text("Mike\n", encoding="utf-8")
    (package / "README.md").write_text("Created by Mike\n", encoding="utf-8")
    row = run_license_gate(str(package), str(tmp_path / "license.jsonl"), str(tmp_path / "report.md"))
    assert row["local_release_ready"] is True
    assert row["public_publish_ready"] is False
