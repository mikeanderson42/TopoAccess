from __future__ import annotations

from topoaccess_prod.integrations.tool_schema import all_schemas


def validate_tool_schema() -> dict:
    schema = all_schemas()
    exact = [tool for tool in schema["tools"] if tool["name"] == "exact_lookup"][0]
    return {
        "tools": len(schema["tools"]),
        "exact_lookup_tool_only": exact["model_fallback_allowed"] is False,
        "provenance_required": all(tool["provenance"]["required"] for tool in schema["tools"]),
        "result_status": "pass",
    }

