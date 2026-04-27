from pathlib import Path

from topoaccess_prod.harness.codex_fixture_loop import run_codex_fixture_loop


def test_codex_fixture_loop_rows(tmp_path: Path):
    rows = run_codex_fixture_loop("default", 2, 1, 1, str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert len(rows) == 2
    assert all(row["result_status"] == "pass" for row in rows)

