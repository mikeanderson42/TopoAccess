from topoaccess_prod.harness.workspace import detect_workspace, list_profiles


def test_workspace_profiles():
    assert list_profiles()[0]["name"] == "default"
    assert detect_workspace(".")["detected"] is True
