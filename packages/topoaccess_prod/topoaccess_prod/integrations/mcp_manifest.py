from __future__ import annotations

import json


def mcp_manifest() -> dict:
    return {
        "name": "topoaccess",
        "tools": [
            {"name": "exact_lookup", "model_fallback_allowed": False, "provenance_required": True},
            {"name": "test_impact", "model_fallback_allowed": False, "provenance_required": True},
            {"name": "change_plan", "model_fallback_allowed": True, "category_gate": "change_planning", "provenance_required": True},
            {"name": "post_edit_validate", "read_only": True, "model_fallback_allowed": False, "provenance_required": True},
        ],
    }


def stdio_schema() -> dict:
    return {"transport": "stdio", "request": {"tool": "string", "profile": "string", "input": "object"}, "response": {"provenance": "array", "safety": "object", "unsupported": "boolean"}}

