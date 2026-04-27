from types import SimpleNamespace

from topoaccess_prod.harness import regression_matrix


def test_regression_matrix_keeps_topoaccess_and_legacy_commands(monkeypatch, tmp_path):
    monkeypatch.setattr(regression_matrix.subprocess, "run", lambda *args, **kwargs: SimpleNamespace(returncode=0, stdout="", stderr=""))
    rows = regression_matrix.run_regression_matrix("demo", tmp_path / "matrix.jsonl", tmp_path / "report.md")
    commands = [row["command"] for row in rows]
    assert any(command.startswith("topoaccess --help") for command in commands)
    assert any("topoaccess_agent.py" in command for command in commands)
    assert all(row["result_status"] == "pass" for row in rows)
