from pathlib import Path

from topoaccess_prod.install.install_wizard import run_install_wizard


def test_install_wizard_dry_run(tmp_path: Path):
    row = run_install_wizard("default", ".", "missing-cache", "missing-search", True, str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert row["dry_run"] is True
    assert row["result_status"] == "pass"

