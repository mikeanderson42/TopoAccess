from __future__ import annotations

import json
from pathlib import Path

from .first_run import DEFAULT_CACHE, DEFAULT_PROFILE, run_first_init


def suggested_fixes(cache: str, preferred_search: str, profile: str = "default") -> list[str]:
    fixes = []
    if not Path(cache).exists():
        fixes.append("Cache missing: rerun the latest cache build or point --cache at an existing TopoAccess cache.")
    if not Path(preferred_search).exists():
        fixes.append("Preferred-search missing: run topoaccess init or provide a workspace profile search file.")
    if not Path("packages/topoaccess_prod/configs/workspaces.yaml").exists():
        fixes.append(f"Workspace profile missing: run topoaccess init or topoaccess workspace init --profile {profile}.")
    if not fixes:
        fixes.append("No automatic fixes required.")
    return fixes


def apply_safe_doctor_fixes(profile: str = DEFAULT_PROFILE) -> dict:
    """Apply only local, model-free repairs for a fresh clone."""
    changed: list[str] = []
    topo_dir = Path(".topoaccess")
    if not topo_dir.exists():
        topo_dir.mkdir(parents=True)
        changed.append(".topoaccess/")
    cache = Path(DEFAULT_CACHE)
    if not cache.exists():
        cache.mkdir(parents=True)
        changed.append(DEFAULT_CACHE)
    config = topo_dir / "config.example.json"
    if not config.exists():
        config.write_text(
            json.dumps(
                {
                    "profile": profile,
                    "cache": DEFAULT_CACHE,
                    "model_required": False,
                    "model_backed_synthesis": "optional_category_gated",
                    "exact_lookup_tool_only": True,
                },
                indent=2,
                sort_keys=True,
            )
            + "\n",
            encoding="utf-8",
        )
        changed.append(str(config))
    init = run_first_init(profile=profile)
    return {
        "command": "topoaccess doctor --fix",
        "profile": profile,
        "changed": changed,
        "workspace": init,
        "disallowed_actions": [
            "no model installation",
            "no git push",
            "no shell profile edits",
            "no external harness config edits",
        ],
        "result_status": "pass",
    }
