from __future__ import annotations

from .generic_agent_adapter import command_recommendation, context_pack, post_edit, test_recommendation


def codex_brief(task: str, profile: str = "default") -> dict:
    pack = context_pack(task, mode="codex")
    return {
        "mission_brief": task,
        "relevant_files": pack["relevant_files"],
        "tests_to_run": pack["tests"],
        "commands": pack["commands"],
        "provenance": pack["provenance"],
        "risks": pack["risks"],
        "context_pack": pack,
        "post_edit_validation_plan": "Run topoaccess_agent.py post-edit with changed files, then product tests.",
    }


def codex_post_edit(changed_files: list[str]) -> dict:
    return post_edit(changed_files)
