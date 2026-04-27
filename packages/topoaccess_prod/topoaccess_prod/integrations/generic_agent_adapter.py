from __future__ import annotations

from ..harness.post_edit_validation import validate_post_edit
from ..harness.preflight import preflight
from ..harness.prompt_pack import build_prompt_pack


def preflight_query(task: str, profile: str = "default") -> dict:
    return preflight(task, profile)


def context_pack(task: str, mode: str = "standard") -> dict:
    return build_prompt_pack(task, mode=mode)


def test_recommendation(changed_file: str) -> dict:
    return {"changed_file": changed_file, "tests": ["python -m pytest packages/topoaccess_prod/tests"], "provenance": ["packages/topoaccess_prod/tests"]}


def command_recommendation(task: str) -> dict:
    return {"task": task, "command": "python -m pytest packages/topoaccess_prod/tests", "provenance": ["packages/topoaccess_prod/tests"]}


def post_edit(changed_files: list[str]) -> dict:
    return validate_post_edit(changed_files)
