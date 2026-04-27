from __future__ import annotations

from pathlib import Path


def suggested_fixes(cache: str, preferred_search: str, profile: str = "default") -> list[str]:
    fixes = []
    if not Path(cache).exists():
        fixes.append("Cache missing: rerun the latest cache build or point --cache at an existing TopoAccess cache.")
    if not Path(preferred_search).exists():
        fixes.append("Preferred-search missing: rerun V22 preferred model search or provide runs/topoaccess_v22/preferred_model_search.jsonl.")
    if not Path("packages/topoaccess_prod/configs/workspaces.yaml").exists():
        fixes.append(f"Workspace profile missing: run topoaccess_workspace.py init --profile {profile}.")
    if not fixes:
        fixes.append("No automatic fixes required.")
    return fixes

