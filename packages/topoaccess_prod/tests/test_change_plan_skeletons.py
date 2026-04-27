from pathlib import Path

from topoaccess_prod.harness.change_plan_skeletons import optimize_skeleton


def test_change_plan_skeleton_improves_to_target(tmp_path: Path):
    row = optimize_skeleton("default", 0.9564, 0.96, str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert row["change_planning_score"] > 0.96

