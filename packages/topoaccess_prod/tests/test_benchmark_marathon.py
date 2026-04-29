from topoaccess_prod.harness.benchmark_marathon import generate_row, run_marathon


def test_generate_row_has_required_fields():
    row = generate_row(0, "demo", 1337, ["topoaccess_tool_only"], ["exact_lookup"])
    assert row["run_id"] == "topoaccess_prod_v44"
    assert row["exact_lookup_tool_only"] is True
    assert row["model_invoked"] is False
    assert row["token_savings"] > 0.9
    assert row["wrong_high_confidence"] == 0
    assert row["unsupported_high_confidence"] == 0


def test_run_marathon_writes_rows(tmp_path):
    out = tmp_path / "bench.jsonl"
    rows = run_marathon("demo", 12, 12, 5, 7, ["topoaccess_tool_only"], ["exact_lookup", "unsupported"], out, tmp_path / "chunks", tmp_path / "summary.json", tmp_path / "report.md")
    assert len(rows) == 12
    assert out.exists()
    assert (tmp_path / "summary.json").exists()
    assert all("direct_tokens_estimate" in row for row in rows)


def test_run_marathon_large_result_does_not_retain_all_rows(tmp_path):
    out = tmp_path / "bench.jsonl"
    result = run_marathon("demo", 6000, 6000, 500, 7, ["topoaccess_tool_only"], ["exact_lookup"], out, tmp_path / "chunks", tmp_path / "summary.json", tmp_path / "report.md")
    assert len(result) == 6000
    assert result.rows is None
    assert sum(1 for _ in out.open(encoding="utf-8")) == 6000
