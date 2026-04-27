from __future__ import annotations

from .generic_agent_adapter import context_pack
from .tool_schema import all_schemas


def claude_tool_spec(task: str) -> dict:
    return {"adapter": "claude_code", "tool_schema": all_schemas(), "prompt_context_pack": context_pack(task, mode="claude"), "post_edit_command": "python packages/topoaccess_prod/scripts/topoaccess_agent.py post-edit --profile default --changed-files <files>"}
