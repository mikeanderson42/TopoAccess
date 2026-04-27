from topoaccess_prod.harness.adversarial_benchmark import make_result_row, run_adversarial_benchmark


def test_adversarial_row_preserves_exact_lookup_tool_only():
    row = make_result_row(
        run_id="test",
        seed=1,
        phase="unit",
        fixture_repo="fixture",
        scenario_id="scenario",
        command="topoaccess query",
        cli_mode="topoaccess",
        category="exact_lookup",
        route="tool",
        model_invoked=False,
    )
    assert row["exact_lookup_tool_only"] is True
    assert row["model_invoked"] is False
    assert row["wrong_high_confidence"] == 0
    assert row["unsupported_high_confidence"] == 0


def test_adversarial_benchmark_writes_rows(tmp_path):
    fixture = tmp_path / "fixtures" / "repo_a"
    fixture.mkdir(parents=True)
    rows = run_adversarial_benchmark([str(tmp_path / "fixtures")], 12, 12, 5, 7, tmp_path / "rows.jsonl", tmp_path / "report.md")
    assert len(rows) == 12
    assert (tmp_path / "rows.jsonl").exists()
    assert all(row["hallucinated_file_count"] == 0 for row in rows)
