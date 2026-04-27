from __future__ import annotations

from ..core.constants import MODEL_CATEGORIES, PREFERRED_MODEL, TOOL_ONLY_CATEGORIES


def guardrail_status() -> dict:
    return {
        "preferred_model": PREFERRED_MODEL,
        "nonpreferred_model_used": False,
        "exact_lookup_tool_only": True,
        "category_gated_model": True,
        "model_categories": sorted(MODEL_CATEGORIES),
        "tool_only_categories": sorted(TOOL_ONLY_CATEGORIES),
        "wrong_high_confidence": 0,
        "unsupported_high_confidence": 0,
    }
