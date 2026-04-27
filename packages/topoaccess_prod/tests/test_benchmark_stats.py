from topoaccess_prod.harness.benchmark_marathon import generate_row
from topoaccess_prod.harness.benchmark_stats import summarize_rows


def test_summary_computes_token_and_latency_stats():
    rows = [generate_row(i, "demo", 42, ["topoaccess_tool_only"], ["exact_lookup", "change_planning"]) for i in range(20)]
    summary = summarize_rows(rows)
    assert summary["rows"] == 20
    assert summary["average_token_savings"] > 0.85
    assert summary["p95_latency_ms"] >= summary["p50_latency_ms"]
    assert summary["wrong_high_confidence"] == 0
