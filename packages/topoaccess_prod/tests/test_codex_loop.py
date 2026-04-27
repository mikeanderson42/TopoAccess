from topoaccess_prod.harness.codex_loop import codex_loop_row


def test_codex_loop_saves_tokens_and_keeps_provenance():
    row = codex_loop_row(0, "default")
    assert row["token_savings"] > 0.9
    assert row["provenance_count"] >= 1
    assert row["hallucinated_files"] == 0
