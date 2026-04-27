from pathlib import Path

from topoaccess_prod.release.remote_setup import remote_setup


def test_remote_setup_reports_manual_or_configured(tmp_path: Path):
    row = remote_setup("branch", str(tmp_path), str(tmp_path / "remote.jsonl"), str(tmp_path / "report.md"))
    assert row["result_status"] in {"pass", "manual_required"}
    assert "push_command" in row

