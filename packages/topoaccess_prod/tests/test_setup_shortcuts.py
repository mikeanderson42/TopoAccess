from topoaccess_prod.cli.main import main
from topoaccess_prod.install.harness_setup_shortcuts import run_setup_shortcut


def test_setup_shortcut_is_dry_run_by_default(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = run_setup_shortcut("codex", "demo")
    assert result["result_status"] == "pass"
    assert result["dry_run"] is True
    assert result["external_configs_modified"] is False


def test_setup_apply_is_explicitly_blocked(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = run_setup_shortcut("codex", "demo", dry_run=False, apply=True)
    assert result["result_status"] == "fail"
    assert "--apply" in result["error"]


def test_topoaccess_setup_aliases(capsys):
    assert main(["setup", "claude", "--profile", "demo", "--dry-run"]) == 0
    out = capsys.readouterr().out
    assert "claude-code" in out


def test_setup_supports_all_public_targets(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    for target in ["codex", "claude", "cursor", "aider", "openclaw", "openhands", "hermes", "generic", "http", "stdio"]:
        result = run_setup_shortcut(target, "demo")
        assert result["result_status"] == "pass"
        assert result["external_configs_modified"] is False
        assert "test_command" in result
