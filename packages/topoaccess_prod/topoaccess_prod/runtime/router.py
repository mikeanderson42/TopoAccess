from __future__ import annotations

from ..core.policies import route_for_category


def route(category: str) -> dict:
    selected = route_for_category(category)
    return {"category": category, "route": selected, "exact_lookup_tool_only": selected == "tool_only", "model_category_gate": selected == "category_gated_preferred_model"}
