from topoaccess_prod import PREFERRED_MODEL


def test_product_imports():
    assert "Qwen3.6" in PREFERRED_MODEL
