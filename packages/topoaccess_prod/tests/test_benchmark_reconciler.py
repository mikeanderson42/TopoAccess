from topoaccess_prod.harness.benchmark_reconciler import reconcile


def test_benchmark_reconciler(tmp_path):
    rows = reconcile(str(tmp_path / "b.jsonl"), str(tmp_path / "r.md"))
    assert rows[-1]["result_status"] == "pass"
