from topoaccess_prod.harness.schema_fuzzer import run_schema_fuzz


def test_schema_fuzzer_keeps_exact_lookup_model_free(tmp_path):
    rows = run_schema_fuzz("demo", 25, 25, ["tool_schema", "http", "stdio"], 19, tmp_path / "schema.jsonl", tmp_path / "report.md")
    exact_rows = [row for row in rows if row["category"] == "exact_lookup"]
    assert exact_rows
    assert all(row["model_invoked"] is False for row in exact_rows)
    assert all(row["result_status"] == "pass" for row in rows)
