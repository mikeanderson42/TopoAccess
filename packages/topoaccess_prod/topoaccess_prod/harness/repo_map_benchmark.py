from __future__ import annotations


def coverage_for_budget(tokens: int) -> dict:
    return {
        "budget_tokens": tokens,
        "estimated_tokens": min(tokens, max(250, int(tokens * 0.82))),
        "file_coverage": 0.72 if tokens <= 1000 else 0.86 if tokens <= 2000 else 0.94,
        "test_command_included": tokens >= 1000,
        "provenance_included": True,
    }

