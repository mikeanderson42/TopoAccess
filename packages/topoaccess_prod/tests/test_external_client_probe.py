from topoaccess_prod.harness.external_client_probe import port_available


def test_port_available_returns_bool():
    assert isinstance(port_available(9), bool)
