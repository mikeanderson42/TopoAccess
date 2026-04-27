from pathlib import Path

from topoaccess_prod.release.secret_scan import scan_secrets


def test_secret_scan_flags_private_key(tmp_path: Path):
    marker = "-----BEGIN " + "PRIVATE KEY-----\nabc\n"
    (tmp_path / "key.txt").write_text(marker, encoding="utf-8")
    rows = scan_secrets([str(tmp_path)], str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert any(row["result_status"] == "fail" for row in rows)
