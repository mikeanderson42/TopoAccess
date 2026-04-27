from topoaccess_prod.cli.main import main
from topoaccess_prod.install.try_demo import run_try_demo


def test_try_demo_is_model_free(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = run_try_demo()
    assert result["result_status"] == "pass"
    assert result["model_required"] is False
    assert result["model_invoked"] is False


def test_topoaccess_try_command(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["try"]) == 0
    assert "TopoAccess model-free demo passed" in capsys.readouterr().out
