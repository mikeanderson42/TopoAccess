from topoaccess_prod.harness.dogfood import dogfood_row


def test_dogfood_row_has_safety_and_brief():
    row = dogfood_row(0, "default")
    assert row["codex_brief_generated"] is True
    assert row["post_edit_validation_generated"] is True
    assert row["nonpreferred_model_used"] is False
    assert row["safety_counters"]["wrong_high_confidence"] == 0
