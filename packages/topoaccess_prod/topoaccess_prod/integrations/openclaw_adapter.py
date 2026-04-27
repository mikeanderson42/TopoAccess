from __future__ import annotations

from .generic_agent_adapter import context_pack
from .tool_schema import all_schemas


def openclaw_tool_spec(task: str) -> dict:
    return {"adapter": "openclaw", "tool_schema": all_schemas(), "prompt_context_pack": context_pack(task, mode="openclaw"), "post_edit_command": "python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files <files>"}
