from topoaccess_prod.harness.scenario_benchmark import build_dataset_file, run_scenarios
from topoaccess_prod.harness.scenario_failure_mining import mine_scenario_failures


def test_scenario_failure_mining_groups(tmp_path):
    dataset = tmp_path / "dataset.jsonl"
    build_dataset_file("examples/scenario_repos", dataset, tmp_path / "dataset.md")
    run_scenarios(dataset, 5, 5, 2, 8, None, tmp_path / "rows.jsonl", tmp_path / "summary.json", tmp_path / "report.md")
    groups = mine_scenario_failures(tmp_path / "rows.jsonl", tmp_path / "failures.jsonl", tmp_path / "failures.md")
    assert {g["kind"] for g in groups} >= {"weakest_workflows", "safety_failures"}
