from topoaccess_prod.harness.prompt_pack_optimizer import optimize


def test_prompt_pack_optimizer(tmp_path):
    rows = optimize(["codex"], str(tmp_path / "p.jsonl"), str(tmp_path / "r.md"))
    assert rows[0]["result_status"] == "pass"
