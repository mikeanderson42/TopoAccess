from topoaccess_prod.install.workspace_init import detect_workspace


def test_workspace_detect():
    assert detect_workspace(".")["status"] == "pass"
