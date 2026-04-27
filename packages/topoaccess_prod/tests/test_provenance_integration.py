from topoaccess_prod.core.policies import route_for_category
from topoaccess_prod.harness.post_edit_validation import validate_post_edit
from topoaccess_prod.harness.prompt_pack import build_prompt_pack
from topoaccess_prod.integrations.codex_adapter import codex_brief
from topoaccess_prod.integrations.generic_agent_adapter import preflight_query


def test_build_prompt_pack_preserves_legacy_and_structured_provenance():
    pack = build_prompt_pack("Task")

    assert pack["provenance"]
    assert pack["provenance_entries"]
    assert pack["provenance_verified"] is True
    assert pack["provenance_verification"]["result_status"] == "pass"
    assert "audited_span_text" not in pack["provenance_entries"][0]
    assert "bounded_excerpt" in pack["provenance_entries"][0]


def test_codex_brief_includes_structured_provenance_through_context_pack():
    brief = codex_brief("Improve provenance")

    assert brief["provenance"]
    assert brief["provenance_entries"]
    assert brief["context_pack"]["provenance_entries"] == brief["provenance_entries"]
    assert "audited_span_text" not in str(brief)


def test_preflight_includes_structured_provenance_without_raw_audited_span_text():
    result = preflight_query("Verify provenance payload")
    entries = result["pack"]["provenance_entries"]

    assert entries
    assert "bounded_excerpt" in entries[0]
    assert "audited_span_text" not in str(result)


def test_post_edit_validation_exposes_read_only_validation_posture():
    result = validate_post_edit(["README.md"])

    assert result["result_status"] == "pass"
    assert result["field_mask_scoped"] is True
    assert result["raw_json_diff_authority"] is False
    assert result["span_hash_provenance_supported"] is True
    assert result["field_mask_validation"]["result_status"] == "pass"


def test_route_policy_invariants_remain_unchanged():
    assert route_for_category("exact_lookup") == "tool_only"
    assert route_for_category("change_planning") == "category_gated_preferred_model"
    assert route_for_category("not_a_category") == "safe_abstain"
