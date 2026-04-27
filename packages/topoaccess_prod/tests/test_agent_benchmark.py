from topoaccess_prod.harness.result_scoring import score_result


def test_agent_benchmark_scoring():
    assert score_result("codex_style_with_topoaccess", "exact_lookup")["provenance_correctness"] > score_result("codex_style_without_topoaccess", "exact_lookup")["provenance_correctness"]
