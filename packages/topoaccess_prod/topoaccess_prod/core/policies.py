from __future__ import annotations

from .constants import MODEL_CATEGORIES, TOOL_ONLY_CATEGORIES


def route_for_category(category: str) -> str:
    if category in TOOL_ONLY_CATEGORIES:
        return "tool_only"
    if category in MODEL_CATEGORIES:
        return "category_gated_preferred_model"
    return "safe_abstain"


def exact_lookup_tool_only(category: str) -> bool:
    return category in TOOL_ONLY_CATEGORIES


def model_category_gate(category: str) -> bool:
    return category in MODEL_CATEGORIES
