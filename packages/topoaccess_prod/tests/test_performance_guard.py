from types import SimpleNamespace

from topoaccess_prod.harness import performance_guard


def test_performance_guard_records_bounded_command_results(monkeypatch, tmp_path):
    monkeypatch.setattr(performance_guard.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="", stderr=""))
    rows = performance_guard.run_performance_guard("demo", "", tmp_path / "perf.jsonl", tmp_path / "report.md")
    assert rows
    assert all(row["result_status"] == "pass" for row in rows)
    assert all(row["latency_ms"] < 5000 for row in rows)
