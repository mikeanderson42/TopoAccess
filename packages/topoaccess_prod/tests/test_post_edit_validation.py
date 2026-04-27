from topoaccess_prod.harness.post_edit_validation import validate_post_edit


def test_post_edit_validation():
    result = validate_post_edit(["x.py"])
    assert result["stale_answer_prevented"] is True
