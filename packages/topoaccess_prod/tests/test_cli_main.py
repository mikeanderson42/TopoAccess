from topoaccess_prod.cli.main import main


def test_cli_version_and_commands(capsys):
    assert main(["version"]) == 0
    assert "public_model_agnostic" in capsys.readouterr().out
    assert main(["commands"]) == 0
    assert "codex-brief" in capsys.readouterr().out


def test_cli_workspace_init_and_doctor(tmp_path, capsys, monkeypatch):
    monkeypatch.chdir(tmp_path)
    assert main(["workspace", "init", "--profile", "demo", "--repo", ".", "--cache", ".topoaccess/cache"]) == 0
    assert main(["doctor", "--profile", "demo"]) == 0
    out = capsys.readouterr().out
    assert "doctor_rows" in out
