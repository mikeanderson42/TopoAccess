from topoaccess_prod.core.provenance_index import ProvenanceFileCache, SpanRequest, verify_spans_batch


def test_provenance_file_cache_finds_span(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("one\nneedle line\nthree\n", encoding="utf-8")
    cache = ProvenanceFileCache()
    match = cache.find_span(source, "needle line")
    assert match.matched is True
    assert match.start_line == 2
    assert cache.find_span(source, "needle line").matched is True


def test_provenance_file_cache_abstains_on_large_file(tmp_path):
    source = tmp_path / "large.txt"
    source.write_text("needle", encoding="utf-8")
    match = ProvenanceFileCache().find_span(source, "needle", max_scan_bytes=1)
    assert match.matched is False
    assert match.reason == "unreadable_or_too_large"


def test_verify_spans_batch_reuses_cache(tmp_path):
    source = tmp_path / "doc.md"
    source.write_text("alpha\nbeta\n", encoding="utf-8")
    matches = verify_spans_batch([SpanRequest(source, "alpha"), SpanRequest(source, "beta")])
    assert [match.matched for match in matches] == [True, True]
