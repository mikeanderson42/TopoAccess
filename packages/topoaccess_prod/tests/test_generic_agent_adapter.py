from topoaccess_prod.integrations.generic_agent_adapter import preflight_query


def test_generic_preflight_pack():
    result = preflight_query("Add report")
    assert result["pack"]["context_pack_tokens"] < 2000
