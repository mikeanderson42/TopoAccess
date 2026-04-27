from topoaccess_prod.release.fresh_install import run_fresh_install_smoke


def test_fresh_install_module_importable():
    assert callable(run_fresh_install_smoke)

