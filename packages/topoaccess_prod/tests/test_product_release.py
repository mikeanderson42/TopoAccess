from pathlib import Path

from topoaccess_prod.cli.topoaccessctl import run_command


def test_product_release_manifest_generation(tmp_path):
    release = tmp_path / "release"
    result = run_command("validate-release", release=str(release))
    assert result["status"] == "pass"
    assert (release / "release_manifest.json").exists()
