from topoaccess_prod.install.multi_repo_registry import registry_status


def test_multi_repo_registry():
    assert registry_status()["multi_repo_ready"] is True
