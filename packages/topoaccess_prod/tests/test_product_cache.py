from topoaccess_prod.cache.store import cache_status
from topoaccess_prod.cache.store import cache_exists, cache_manifest_path, validate_cache_reference


def test_product_cache_status():
    assert cache_status()["stale_answer_prevented"] is True


def test_product_cache_missing_is_model_free():
    status = cache_status()
    assert status["status"] == "missing"
    assert status["cache_exists"] is False
    assert status["mutated"] is False
    assert status["exact_lookup_tool_only"] is True


def test_product_cache_fixture(tmp_path):
    cache_dir = tmp_path / "cache"
    cache_dir.mkdir()
    manifest = cache_dir / "manifest.json"
    manifest.write_text('{"cache_hash": "fixture", "cache_hit_rate": 0.5}', encoding="utf-8")

    assert cache_exists(cache_dir) is True
    assert cache_manifest_path(cache_dir).endswith("manifest.json")
    assert validate_cache_reference(cache_dir)["manifest_exists"] is True
    status = cache_status(cache_dir)
    assert status["cache_hash"] == "fixture"
    assert status["cache_hit_rate"] == 0.5
    assert status["stale_answer_prevented"] is True
