from pathlib import Path

from topoaccess_prod.release.secret_scan import scan_secrets


def test_secret_scan_flags_private_key(tmp_path: Path):
    marker = "-----BEGIN " + "PRIVATE KEY-----\nabc\n"
    (tmp_path / "key.txt").write_text(marker, encoding="utf-8")
    rows = scan_secrets([str(tmp_path)], str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert any(row["result_status"] == "fail" for row in rows)


def test_secret_scan_skips_large_file(tmp_path: Path):
    big = tmp_path / "big.txt"
    big.write_text("x" * 32, encoding="utf-8")
    rows = scan_secrets([str(tmp_path)], str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"), max_file_bytes=8)
    assert any(row.get("skipped_reason") == "too_large" for row in rows)


def test_secret_scan_detects_secret_in_chunk(tmp_path: Path):
    token = "api_key = '" + "x" * 20 + "'"
    (tmp_path / "settings.txt").write_text("a" * 70000 + token, encoding="utf-8")
    rows = scan_secrets([str(tmp_path)], str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"), max_file_bytes=100000)
    assert any(row["result_status"] == "fail" for row in rows)
