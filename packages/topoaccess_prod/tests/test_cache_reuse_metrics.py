from topoaccess_prod.harness.cache_reuse_metrics import cache_hit, cache_reuse_count


def test_cache_reuse_increases_after_first_topoaccess_step():
    assert cache_reuse_count(1, "topoaccess_tool_only") == 0
    assert cache_reuse_count(3, "topoaccess_tool_only") == 2
    assert cache_hit(3, "topoaccess_tool_only") is True
    assert cache_hit(3, "broad_context_baseline") is False
