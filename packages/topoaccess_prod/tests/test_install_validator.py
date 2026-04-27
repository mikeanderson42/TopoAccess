from pathlib import Path

from topoaccess_prod.harness.install_validator import validate_install_snippets


def test_install_validator_detects_missing(tmp_path: Path):
    result = validate_install_snippets(str(tmp_path))
    assert result["result_status"] == "fail"
    assert result["missing"]
