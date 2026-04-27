from topoaccess_prod.integrations.tool_schema import all_schemas


def test_exact_lookup_forbids_model_fallback():
    exact = next(t for t in all_schemas()["tools"] if t["name"] == "exact_lookup")
    assert exact["model_fallback_allowed"] is False
