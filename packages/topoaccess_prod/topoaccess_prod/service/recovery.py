from __future__ import annotations


def recovery_status() -> dict:
    return {"recovery_ready": True, "fallback": "safe_abstain_or_tool_only", "nonpreferred_model_used": False}
