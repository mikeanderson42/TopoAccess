from topoaccess_prod.harness.benchmark_marathon import run_marathon
from topoaccess_prod.harness.failure_mining import mine_failures


def test_failure_mining_outputs_groups(tmp_path):
    bench = tmp_path / "bench.jsonl"
    run_marathon("demo", 30, 30, 10, 9, None, None, bench, tmp_path / "chunks", tmp_path / "summary.json", tmp_path / "report.md")
    rows = mine_failures(bench, tmp_path / "failures.jsonl", tmp_path / "failures.md")
    assert {row["kind"] for row in rows} >= {"lowest_token_savings", "slowest_routes", "hallucinations"}
    assert (tmp_path / "failures.md").exists()
