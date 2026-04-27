from topoaccess_prod.harness.scenario_fixtures import build_dataset
from topoaccess_prod.harness.workflow_scorer import score_step, selection_score


def test_workflow_scorer_prefers_topoaccess_selection():
    scenario = build_dataset("examples/scenario_repos")[0]
    row = score_step(scenario, "topoaccess_tool_only", 2, "test_impact", 99)
    assert row["cache_reuse_count"] == 1
    assert selection_score(row["files_selected"], row["expected_files"]) == 1.0
    assert row["wrong_high_confidence"] == 0
