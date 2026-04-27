from topoaccess_prod.harness.real_agent_soak import run_soak


def test_real_agent_soak(tmp_path):
    rows = run_soak(2, 2, ["codex_with_topoaccess"], str(tmp_path / "s.jsonl"), str(tmp_path / "r.md"))
    assert rows[0]["hallucinated_file_count"] == 0
