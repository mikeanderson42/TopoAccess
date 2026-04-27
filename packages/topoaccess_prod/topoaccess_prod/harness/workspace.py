from __future__ import annotations

import json
from pathlib import Path


DEFAULT_PROFILE = {
    "name": "default",
    "repo_root": ".",
    "cache_path": "cache/topoaccess_v21",
    "release_path": "release/topoaccess_prod",
    "preferred_model_search": "runs/topoaccess_v22/preferred_model_search.jsonl",
    "service_port": 8765,
    "default_policy": "final_default_policy",
    "exact_lookup_policy": "tool_only",
    "category_model_policy": "category_gated_preferred_model",
    "dashboard_path": "release/topoaccess_prod/dashboard.json",
}


def list_profiles() -> list[dict]:
    return [DEFAULT_PROFILE]


def detect_workspace(repo: str = ".") -> dict:
    root = Path(repo).resolve()
    return {**DEFAULT_PROFILE, "repo_root": str(root), "detected": (root / "packages" / "topoaccess_prod").exists()}


def profile_status(profile: str = "default") -> dict:
    current = DEFAULT_PROFILE if profile == "default" else {**DEFAULT_PROFILE, "name": profile}
    return {**current, "status": "pass", "workspace_profiles": True}


def write_profiles(path: str | Path) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text(json.dumps(list_profiles(), indent=2, sort_keys=True) + "\n", encoding="utf-8")
