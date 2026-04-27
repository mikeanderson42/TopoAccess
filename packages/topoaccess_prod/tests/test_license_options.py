from topoaccess_prod.release.license_options import OPTIONS


def test_license_options_include_private_placeholder():
    assert any(option["id"] == "internal-private" for option in OPTIONS)

