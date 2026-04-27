from __future__ import annotations

from pathlib import Path

from ..harness.post_edit_validation import validate_post_edit
from ..integrations.codex_adapter import codex_brief
from ..integrations.http_tool_server import handle_tool
from .first_run import run_first_init


def run_try_demo(profile: str = "demo", repo: str = ".") -> dict:
    """Run a self-contained model-free demo suitable for a fresh clone."""
    init = run_first_init(profile=profile, repo=repo)
    exact = handle_tool("/query", {"query": "Where is the CLI entrypoint?", "profile": profile})
    brief = codex_brief("What tests should I run after editing README.md?", profile)
    post_edit = validate_post_edit(["README.md"])
    checks = [
        {"name": "package/import", "result_status": "pass"},
        {"name": "workspace init", "result_status": init["result_status"]},
        {"name": "exact/tool route smoke", "result_status": "pass" if exact.get("status", "pass") != "fail" else "fail"},
        {"name": "codex brief smoke", "result_status": "pass" if brief.get("provenance") else "fail"},
        {"name": "post-edit validation smoke", "result_status": post_edit.get("result_status", "fail")},
    ]
    failures = [check for check in checks if check["result_status"] != "pass"]
    return {
        "command": "topoaccess try",
        "profile": profile,
        "repo": str(Path(repo).resolve()),
        "checks": checks,
        "model_required": False,
        "model_invoked": False,
        "exact_lookup_tool_only": True,
        "summary": "TopoAccess model-free demo passed." if not failures else "TopoAccess demo found failures.",
        "next_commands": init["next_commands"],
        "result_status": "pass" if not failures else "fail",
    }
