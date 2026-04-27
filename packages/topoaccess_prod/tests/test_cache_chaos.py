from topoaccess_prod.harness.cache_chaos import run_cache_chaos


def test_cache_chaos_handles_missing_and_stale_states(tmp_path):
    rows = run_cache_chaos("demo", tmp_path / "fixture", 20, 20, 11, tmp_path / "cache.jsonl", tmp_path / "report.md")
    states = {row["cache_state"] for row in rows}
    assert "missing_cache" in states
    assert "corrupted_manifest" in states
    assert all(row["stale_cache_prevented"] for row in rows)
    assert all(row["result_status"] == "pass" for row in rows)
