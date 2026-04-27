from topoaccess_prod.safety.guardrails import guardrail_status


def test_product_guardrails():
    status = guardrail_status()
    assert status["nonpreferred_model_used"] is False
    assert status["exact_lookup_tool_only"] is True
