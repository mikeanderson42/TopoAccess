from __future__ import annotations


def build_context(query: str, category: str) -> dict:
    return {"query": query, "category": category, "context_mode": "balanced_2hop_medium", "provenance_required": True}
