from __future__ import annotations

from .prompt_pack import build_prompt_pack


def preflight(task: str, profile: str = "default") -> dict:
    pack = build_prompt_pack(task, mode="standard")
    return {"profile": profile, "preflight": True, "pack": pack}
