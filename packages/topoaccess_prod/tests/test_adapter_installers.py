from topoaccess_prod.integrations.codex_installer import install


def test_adapter_installer():
    assert install()["result_status"] == "pass"
