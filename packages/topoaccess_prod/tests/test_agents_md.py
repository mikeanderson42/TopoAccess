from topoaccess_prod.integrations.agents_md import BODY, base_row


def test_agents_md_contains_required_policy():
    assert "exact lookup is tool-only" in BODY
    assert "post-edit validation" in BODY
    assert base_row("agents_md", "x")["nonpreferred_model_used"] is False

