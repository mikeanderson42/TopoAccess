from topoaccess_prod.core.field_mask import field_mask_diff, flatten_json_paths


def test_flatten_json_paths_handles_nested_dicts_and_lists():
    assert flatten_json_paths({"a": {"b": [1, {"c": 2}]}}) == {"a.b.0": 1, "a.b.1.c": 2}


def test_field_mask_diff_passes_for_allowed_path_changes():
    before = {"status": "pending", "metadata": {"owner": "topoaccess"}}
    after = {"status": "pass", "metadata": {"owner": "topoaccess"}}

    result = field_mask_diff(before, after, ["status"])

    assert result["result_status"] == "pass"
    assert result["allowed_changes"][0]["path"] == "status"
    assert result["unauthorized_changes"] == []


def test_field_mask_diff_fails_for_unauthorized_changes():
    before = {"status": "pending", "metadata": {"owner": "topoaccess"}}
    after = {"status": "pass", "metadata": {"owner": "other"}}

    result = field_mask_diff(before, after, ["/status"])

    assert result["result_status"] == "fail"
    assert result["unauthorized_changes"][0]["path"] == "metadata.owner"


def test_field_mask_diff_failure_overrides_other_verified_context():
    before = {"answer": {"status": "pass", "source_uri": "doc.md"}, "audit": {"span_verified": True}}
    after = {"answer": {"status": "pass", "source_uri": "other.md"}, "audit": {"span_verified": True}}

    result = field_mask_diff(before, after, ["audit.span_verified"])

    assert result["result_status"] == "fail"
    assert result["unauthorized_changes"][0]["path"] == "answer.source_uri"
