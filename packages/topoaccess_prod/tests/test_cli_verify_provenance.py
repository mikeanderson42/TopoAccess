from topoaccess_prod.cli.main import main


def test_cli_verify_provenance_outputs_verified_entry(capsys, tmp_path, monkeypatch):
    source = tmp_path / "sample.py"
    source.write_text("alpha\nbeta\n", encoding="utf-8")
    monkeypatch.chdir(tmp_path)

    code = main(["verify-provenance", "--path", "sample.py", "--start-line", "1", "--end-line", "1"])
    captured = capsys.readouterr().out

    assert code == 0
    assert '"span_hash"' in captured
    assert '"bounded_excerpt"' in captured
    assert "audited_span_text" not in captured
    assert '"result_status": "pass"' in captured
