from topoaccess_prod.cli.main import main
from topoaccess_prod.install.doctor_fixes import apply_safe_doctor_fixes


def test_doctor_fix_only_creates_local_topoaccess_files(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    result = apply_safe_doctor_fixes("demo")
    assert result["result_status"] == "pass"
    assert (tmp_path / ".topoaccess" / "cache").exists()
    assert (tmp_path / ".topoaccess" / "config.example.json").exists()
    assert "no model installation" in result["disallowed_actions"]


def test_topoaccess_doctor_fix_command(tmp_path, monkeypatch, capsys):
    monkeypatch.chdir(tmp_path)
    assert main(["doctor", "--profile", "demo", "--fix"]) == 0
    assert "fix_result" in capsys.readouterr().out
