from topoaccess_prod.harness.preflight import preflight


def test_preflight():
    assert preflight("Task")["preflight"] is True
