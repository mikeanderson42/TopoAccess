from topoaccess_prod.cli.main import main
from topoaccess_prod.install.first_run import run_first_init


def test_first_run_init_creates_demo_workspace(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = run_first_init()
    assert result["result_status"] == "pass"
    assert (tmp_path / ".topoaccess" / "cache").exists()
    assert result["model_required"] is False


def test_topoaccess_init_command(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["init"]) == 0
    out = capsys.readouterr().out
    assert "topoaccess try" in out
    assert (tmp_path / ".topoaccess" / "cache").exists()
