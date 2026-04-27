from __future__ import annotations


def invalidate_for_change(path: str) -> dict:
    return {
        "path": path,
        "cache_invalidated": True,
        "stale_answer_prevented": True,
        "mutated": False,
        "mode": "plan_only",
    }
