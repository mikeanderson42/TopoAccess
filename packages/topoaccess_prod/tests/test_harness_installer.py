from topoaccess_prod.install.harness_installer import install_target


def test_harness_installer_dry_run():
    assert install_target("codex")["dry_run"] is True
