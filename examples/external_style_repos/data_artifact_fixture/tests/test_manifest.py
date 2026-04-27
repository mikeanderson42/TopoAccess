from src.manifest import artifact_manifest


def test_artifact_manifest():
    assert artifact_manifest()["rows"] == 128
