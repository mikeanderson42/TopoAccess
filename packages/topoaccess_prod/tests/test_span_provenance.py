from __future__ import annotations

from topoaccess_prod.core.provenance import (
    make_span_provenance,
    verify_provenance_entries,
    verify_span_provenance,
)


def test_make_span_provenance_creates_hashes_and_offsets(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")

    entry = make_span_provenance(source, 1, 2, repo_root=tmp_path)

    assert entry["source_uri"] == "sample.py"
    assert entry["start_byte"] == 0
    assert entry["end_byte"] == len("alpha\nbeta\n".encode("utf-8"))
    assert entry["span_byte_length"] == len("alpha\nbeta\n".encode("utf-8"))
    assert entry["span_line_count"] == 2
    assert entry["span_hash"].startswith("sha256:")
    assert entry["content_hash"].startswith("sha256:")
    assert entry["bounded_excerpt"] == "alpha\nbeta\n"
    assert entry["excerpt_truncated"] is False
    assert "audited_span_text" not in entry
    assert entry["verified"] is True


def test_verify_span_provenance_passes_for_unchanged_content(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
    entry = make_span_provenance("sample.py", 2, 2, repo_root=tmp_path)

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "pass"
    assert result["reason"] == "pass_original_offset"
    assert result["winning_tier"] == "exact_offset"
    assert result["confidence"] == 1.0
    assert result["score_gap"] == 0.0
    assert result["candidate_count"] == 0
    assert result["calibration_status"] == "not_sampled"
    assert result["actual_span_hash"] == entry["span_hash"]


def test_verify_span_provenance_fails_after_span_changes(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
    entry = make_span_provenance("sample.py", 2, 2, repo_root=tmp_path)
    source.write_text("alpha\nchanged\ngamma\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "fail"
    assert result["reason"] == "fail_missing_force_reaudit"


def test_verify_provenance_entries_requires_span_hash_for_structured_source(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text("alpha\n", encoding="utf-8")

    result = verify_provenance_entries([{"source_uri": "sample.py", "start_line": 1, "end_line": 1}], repo_root=tmp_path)

    assert result["result_status"] == "fail"
    assert result["failures"][0]["reason"] == "missing span_hash"


def test_legacy_string_provenance_remains_compatible(tmp_path):
    result = verify_provenance_entries(["legacy/path.txt"], repo_root=tmp_path)

    assert result["result_status"] == "pass"
    assert result["legacy_count"] == 1


def test_verify_span_provenance_passes_when_span_moves_in_same_source(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("intro\nstable audited span\noutro\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 2, 2, repo_root=tmp_path)
    source.write_text("new heading\nintro\nstable audited span\noutro\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "pass"
    assert result["reason"] == "pass_relocated_unique"
    assert result["winning_tier"] == "relocated_unique"
    assert result["confidence"] == 1.0
    assert result["candidate_count"] == 1
    assert result["location_changed"] is True
    assert result["current_location"]["start_line"] == 3
    assert result["expected_span_hash"] == entry["span_hash"]
    assert result["actual_span_hash"] == entry["span_hash"]


def test_verify_span_provenance_fails_when_audited_span_missing(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("intro\nstable audited span\noutro\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 2, 2, repo_root=tmp_path)
    source.write_text("intro\nreplacement span\noutro\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "fail"
    assert result["reason"] == "fail_missing_force_reaudit"
    assert result["location_changed"] is False


def test_verify_span_provenance_passes_when_source_changes_but_original_offset_matches(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("intro\nstable audited span\noutro\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 2, 2, repo_root=tmp_path)
    source.write_text("intro\nstable audited span\nchanged outro\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "pass"
    assert result["reason"] == "pass_original_offset"
    assert result["location_changed"] is False
    assert result["actual_span_hash"] == entry["span_hash"]


def test_verify_span_provenance_passes_multi_match_with_context_anchor_winner(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("# A\nbefore\ntarget\nafter\n# B\ntarget\nother\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 3, 3, repo_root=tmp_path)
    source.write_text("# B\ntarget\nother\n# A\nbefore\ntarget\nafter\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "pass"
    assert result["reason"] == "pass_relocated_scored"
    assert result["winning_tier"] == "relocated_scored"
    assert result["location_changed"] is True
    assert result["current_location"]["start_line"] == 6
    assert result["relocation_score"] >= 0.85
    assert result["relocation_score_gap"] >= 0.20
    assert result["confidence"] == result["relocation_score"]
    assert result["score_gap"] == result["relocation_score_gap"]
    assert result["context_anchor_matched"] is True


def test_verify_span_provenance_fails_multi_match_below_confidence_floor(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("# A\ntarget\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 2, 2, repo_root=tmp_path)
    source.write_text("# B\npad\ntarget\n# A\ntarget\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "fail"
    assert result["reason"] == "fail_ambiguous_force_reaudit"
    assert result["winning_tier"] == "ambiguous_force_reaudit"


def test_verify_span_provenance_fails_repeated_headers_with_no_anchor_match(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("xx\ntarget\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 2, 2, repo_root=tmp_path)
    source.write_text("y\ntarget\ntarget\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "fail"
    assert result["reason"] == "fail_ambiguous_force_reaudit"
    assert result["winning_tier"] == "ambiguous_force_reaudit"


def test_verify_span_provenance_fails_when_moved_span_has_multiple_matches_without_winner(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("target\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 1, 1, repo_root=tmp_path)
    source.write_text("prefix\ntarget\nmiddle\ntarget\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "fail"
    assert result["reason"] == "fail_ambiguous_force_reaudit"
    assert result["winning_tier"] == "ambiguous_force_reaudit"


def test_make_span_provenance_bounds_and_truncates_excerpt(tmp_path):
    source = tmp_path / "long.md"
    source.write_text("x" * 900 + "\n", encoding="utf-8")

    entry = make_span_provenance("long.md", 1, 1, repo_root=tmp_path)

    assert entry["excerpt_truncated"] is True
    assert entry["bounded_excerpt"].endswith("\n...")
    assert len(entry["bounded_excerpt"]) < entry["span_byte_length"]
    assert "audited_span_text" not in entry


def test_deterministic_sample_selection_is_stable_across_runs(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("intro\nstable audited span\noutro\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 2, 2, repo_root=tmp_path)

    first = verify_span_provenance(entry, repo_root=tmp_path)
    second = verify_span_provenance(entry, repo_root=tmp_path)

    assert first["sampled_reaudit"] == second["sampled_reaudit"]
    assert first["sampled_reaudit_result"] == second["sampled_reaudit_result"]
    assert first["calibration_status"] == second["calibration_status"]


def test_sampled_reaudit_failure_fails_closed_for_unanchored_unique_relocation(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("target\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 1, 1, repo_root=tmp_path)
    source.write_text("prefix\ntarget\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path, sample_rate=1.0)

    assert result["sampled_reaudit"] is True
    assert result["sampled_reaudit_result"] == "fail"
    assert result["calibration_status"] == "sampled_fail"
    assert result["result_status"] == "fail"
    assert result["reason"] == "sampled_reaudit_failed_calibration"


def test_unsampled_relocated_unique_pass_remains_pass(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("target\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 1, 1, repo_root=tmp_path)
    source.write_text("prefix\ntarget\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path, sample_rate=0.0)

    assert result["sampled_reaudit"] is False
    assert result["sampled_reaudit_result"] == "not_sampled"
    assert result["calibration_status"] == "not_sampled"
    assert result["result_status"] == "pass"
    assert result["winning_tier"] == "relocated_unique"
