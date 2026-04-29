from topoaccess_prod.harness.scenario_benchmark import build_dataset_file, run_scenarios


def test_scenario_benchmark_writes_rows(tmp_path):
    dataset = tmp_path / "dataset.jsonl"
    build_dataset_file("examples/scenario_repos", dataset, tmp_path / "dataset.md")
    rows = run_scenarios(dataset, 3, 3, 2, 7, ["topoaccess_tool_only"], tmp_path / "rows.jsonl", tmp_path / "summary.json", tmp_path / "report.md")
    assert rows
    assert all("scenario_id" in row for row in rows)
    assert (tmp_path / "summary.json").exists()


def test_scenario_benchmark_large_result_does_not_retain_all_rows(tmp_path):
    dataset = tmp_path / "dataset.jsonl"
    build_dataset_file("examples/scenario_repos", dataset, tmp_path / "dataset.md")
    result = run_scenarios(dataset, 600, 600, 25, 7, ["topoaccess_tool_only"], tmp_path / "rows.jsonl", tmp_path / "summary.json", tmp_path / "report.md")
    assert len(result) > 600
    assert result.rows is None
    assert (tmp_path / "summary.json").exists()
