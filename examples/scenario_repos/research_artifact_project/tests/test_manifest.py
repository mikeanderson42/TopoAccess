from artifacts.manifest import ARTIFACTS


def test_manifest_has_summary():
    assert ARTIFACTS["summary"] == "docs/results.md"
