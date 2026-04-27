from types import SimpleNamespace

from topoaccess_prod.harness import cli_fuzzer


def test_cli_fuzzer_treats_bad_commands_as_expected_errors(monkeypatch, tmp_path):
    def fake_run(command, text, capture_output, timeout):
        return SimpleNamespace(returncode=0 if command in cli_fuzzer.SAFE_COMMANDS else 2, stdout="help", stderr="")

    monkeypatch.setattr(cli_fuzzer.subprocess, "run", fake_run)
    rows = cli_fuzzer.run_cli_fuzz("demo", 9, 9, 13, tmp_path / "cli.jsonl", tmp_path / "report.md")
    assert len(rows) == 9
    assert all(row["result_status"] == "pass" for row in rows)
