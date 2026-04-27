from pathlib import Path

from topoaccess_prod.integrations.reranker_adapter import lexical_score, reranker_smoke


def test_reranker_lexical_and_smoke(tmp_path: Path):
    assert lexical_score("topoaccess repo", "repo topoaccess cache") > 0
    rows = reranker_smoke("default", ["none", "lexical"], str(tmp_path / "rerank.jsonl"), str(tmp_path / "report.md"))
    assert len(rows) == 2
    assert all(row["nonpreferred_model_used"] is False for row in rows)

