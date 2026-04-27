from pathlib import Path

from topoaccess_prod.harness.claims_audit import audit_claims, claims_gate_passed


def test_claims_audit_allows_model_free_exact_lookup_exception(tmp_path: Path):
    doc = tmp_path / "README.md"
    doc.write_text("Exact lookup never requires a model.\n", encoding="utf-8")
    rows = audit_claims([doc])
    assert claims_gate_passed(rows)


def test_claims_audit_flags_unqualified_guarantee(tmp_path: Path):
    doc = tmp_path / "README.md"
    doc.write_text("This guarantees perfect production savings.\n", encoding="utf-8")
    rows = audit_claims([doc])
    assert not claims_gate_passed(rows)
