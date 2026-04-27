from __future__ import annotations

from .workspace_init import list_workspaces


def registry_status() -> dict:
    return {"workspace_count": len(list_workspaces()), "multi_repo_ready": True}
