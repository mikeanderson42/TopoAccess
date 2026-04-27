from pathlib import Path

from topoaccess_prod.release.artifact_audit import audit_artifacts


def test_artifact_audit_flags_gguf(tmp_path: Path):
    (tmp_path / "model.gguf").write_text("x", encoding="utf-8")
    rows = audit_artifacts([str(tmp_path)], str(tmp_path / "out.jsonl"), str(tmp_path / "r.md"))
    assert any(row["result_status"] == "fail" for row in rows)

