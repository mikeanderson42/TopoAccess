from __future__ import annotations

from pathlib import Path

from .workspace_init import init_workspace, validate_workspace


DEFAULT_PROFILE = "demo"
DEFAULT_CACHE = ".topoaccess/cache"
DEFAULT_SEARCH = ".topoaccess/preferred_model_search.jsonl"


def run_first_init(profile: str = DEFAULT_PROFILE, repo: str = ".", cache: str = DEFAULT_CACHE) -> dict:
    """Create the safe local files a fresh clone needs before first use."""
    Path(".topoaccess").mkdir(parents=True, exist_ok=True)
    Path(cache).mkdir(parents=True, exist_ok=True)
    result = init_workspace(profile, repo, cache, DEFAULT_SEARCH)
    status = validate_workspace(profile)
    return {
        "command": "topoaccess init",
        "profile": profile,
        "repo": result["repo"],
        "cache": cache,
        "workspace_status": status,
        "model_required": False,
        "exact_lookup_tool_only": True,
        "next_commands": [
            "topoaccess try",
            "topoaccess doctor --profile demo",
            'topoaccess codex-brief --profile demo --task "What tests should I run after editing README.md?"',
            "topoaccess post-edit --profile demo --changed-files README.md",
        ],
        "result_status": "pass",
    }
