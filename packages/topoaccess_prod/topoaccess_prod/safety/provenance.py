from __future__ import annotations


def validate_provenance(evidence: list[str] | None = None) -> dict:
    return {"provenance_valid": bool(evidence), "evidence": evidence or []}
