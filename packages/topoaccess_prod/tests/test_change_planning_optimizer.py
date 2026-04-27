from pathlib import Path

from topoaccess_prod.harness.change_planning_optimizer import optimize_change_planning


def test_change_planning_optimizer_improves(tmp_path: Path):
    row = optimize_change_planning("default", 0.9456, str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert row["token_savings"] > row["baseline_token_savings"]
    assert row["provenance_preserved"] is True
