from pathlib import Path

from topoaccess_prod.release.sync_script_guard import inspect_sync_script


def test_sync_guard_detects_push(tmp_path: Path):
    script = tmp_path / "sync_repository.sh"
    script.write_text("#!/usr/bin/env bash\ngit add -A\ngit push origin main\n", encoding="utf-8")
    row = inspect_sync_script([str(script)], "main", True, str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert "git push" in row["dangerous_patterns"]
    assert row["sync_script_used"] is False

