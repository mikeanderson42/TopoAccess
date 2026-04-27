from __future__ import annotations

import json
from pathlib import Path

MODEL_ALLOWED = {"change_plan", "patch_plan", "troubleshooting", "report_synthesis"}
TOOLS = [
    "exact_lookup",
    "symbol_lookup",
    "command_lookup",
    "artifact_lookup",
    "report_fact_lookup",
    "test_impact",
    "change_plan",
    "patch_plan",
    "troubleshooting",
    "report_synthesis",
    "explain_trace",
    "self_check",
    "post_edit_validate",
]


def schema_for(tool: str) -> dict:
    return {
        "name": tool,
        "input": {"query": "string", "workspace_profile": "string"},
        "output": {"answer": "string", "route": "string", "trace_id": "string"},
        "provenance": {"required": True, "fields": ["files", "commands", "reports"]},
        "safety": {"preferred_model_verified": True, "nonpreferred_model_used": False},
        "model_fallback_allowed": tool in MODEL_ALLOWED,
    }


def all_schemas() -> dict:
    return {"version": "topoaccess-prod-v31-agent-harness", "tools": [schema_for(t) for t in TOOLS]}


def write_tool_schema(path: str | Path) -> dict:
    payload = all_schemas()
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(payload, indent=2, sort_keys=True), encoding="utf-8")
    return payload
