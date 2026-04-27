from topoaccess_prod.harness.fixture_mutator import run_fixture_mutations


def test_fixture_mutator_generates_warning_or_adapt_rows(tmp_path):
    fixture_root = tmp_path / "fixtures"
    (fixture_root / "repo_a").mkdir(parents=True)
    rows = run_fixture_mutations([str(fixture_root)], 15, 15, 17, tmp_path / "mutations.jsonl", tmp_path / "report.md")
    assert len(rows) == 15
    assert all(row["actual_behavior"] == "adapt_or_warn_with_provenance" for row in rows)
    assert all(row["model_invoked"] is False for row in rows)
