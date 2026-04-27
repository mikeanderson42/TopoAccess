from topoaccess_prod.cache.store import cache_status


def test_product_cache_status():
    assert cache_status()["stale_answer_prevented"] is True
