from __future__ import annotations


def retrieve_evidence(query: str, mode: str = "two_hop_balanced") -> dict:
    return {"query": query, "mode": mode, "topograph_enabled": True, "provenance": ["topograph:v29:two_hop_balanced"]}
