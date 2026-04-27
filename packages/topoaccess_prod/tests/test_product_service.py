from topoaccess_prod.service.health import health


def test_product_service_health():
    assert health()["preferred_model_verified"] is True
