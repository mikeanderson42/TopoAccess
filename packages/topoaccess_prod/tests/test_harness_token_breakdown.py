from topoaccess_prod.harness.harness_token_breakdown import breakdown_row


def test_harness_token_breakdown_marks_prompt_pack():
    row = breakdown_row("codex", "exact_lookup")
    assert row["prompt_pack"] == "codex"
    assert row["token_savings"] > 0.9
    assert row["nonpreferred_model_used"] is False
