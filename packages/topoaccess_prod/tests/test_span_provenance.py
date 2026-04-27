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
    assert result["actual_span_hash"] == entry["span_hash"]


def test_verify_span_provenance_fails_after_span_changes(tmp_path):
    source = tmp_path / "sample.py"
    source.write_text("alpha\nbeta\ngamma\n", encoding="utf-8")
    entry = make_span_provenance("sample.py", 2, 2, repo_root=tmp_path)
    source.write_text("alpha\nchanged\ngamma\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "fail"
    assert result["reason"] == "audited_span_missing_force_reaudit"


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
    assert result["reason"] == "audited_span_missing_force_reaudit"
    assert result["location_changed"] is False


def test_verify_span_provenance_passes_when_source_changes_but_original_offset_matches(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("intro\nstable audited span\noutro\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 2, 2, repo_root=tmp_path)
    source.write_text("intro\nstable audited span\nchanged outro\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "pass"
    assert result["location_changed"] is False
    assert result["actual_span_hash"] == entry["span_hash"]


def test_verify_span_provenance_fails_when_moved_span_has_multiple_matches(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("target\n", encoding="utf-8")
    entry = make_span_provenance("doc.md", 1, 1, repo_root=tmp_path)
    source.write_text("prefix\ntarget\nmiddle\ntarget\n", encoding="utf-8")

    result = verify_span_provenance(entry, repo_root=tmp_path)

    assert result["result_status"] == "fail"
    assert result["reason"] == "ambiguous_span_location_force_reaudit"


def test_make_span_provenance_bounds_and_truncates_excerpt(tmp_path):
    source = tmp_path / "long.md"
    source.write_text("x" * 900 + "\n", encoding="utf-8")

    entry = make_span_provenance("long.md", 1, 1, repo_root=tmp_path)

    assert entry["excerpt_truncated"] is True
    assert entry["bounded_excerpt"].endswith("\n...")
    assert len(entry["bounded_excerpt"]) < entry["span_byte_length"]
    assert "audited_span_text" not in entry
