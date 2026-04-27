from topoaccess_prod.install.editable_install import editable_install_smoke


def test_editable_install_function_exists():
    assert callable(editable_install_smoke)

