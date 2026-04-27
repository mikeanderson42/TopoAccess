from __future__ import annotations


def abstain(reason: str = "unsupported") -> dict:
    return {"abstained": True, "reason": reason, "model_invoked": False}
