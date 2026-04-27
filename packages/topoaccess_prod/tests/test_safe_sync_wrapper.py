from pathlib import Path

from topoaccess_prod.release.safe_sync_wrapper import ALLOWLIST, safe_sync


def test_safe_sync_uses_allowlist_and_no_unsafe_sync(tmp_path: Path):
    row = safe_sync("branch", str(tmp_path), [str(tmp_path / "missing.sh")], True, str(tmp_path / "out.jsonl"), str(tmp_path / "report.md"))
    assert "packages/topoaccess_prod/" in ALLOWLIST
    assert row["sync_wrapper_used"] is True
    assert row["unsafe_sync_used"] is False
    assert row["push_attempted"] is False

