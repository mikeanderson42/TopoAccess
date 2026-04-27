from __future__ import annotations

import json
from pathlib import Path

WORKSPACE_STATE = Path(".topoaccess/workspaces.jsonl")
LEGACY_WORKSPACE_STATE = Path("runs/topoaccess_prod_v32/workspaces.jsonl")


def init_workspace(profile: str, repo: str, cache: str, preferred_search: str) -> dict:
    Path(cache).mkdir(parents=True, exist_ok=True)
    row = {
        "profile": profile,
        "repo": str(Path(repo).resolve()),
        "cache": cache,
        "preferred_search": preferred_search,
        "model_required": False,
        "model_backed_synthesis": "optional_category_gated",
        "status": "pass",
    }
    WORKSPACE_STATE.parent.mkdir(parents=True, exist_ok=True)
    with WORKSPACE_STATE.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
    return row


def detect_workspace(repo: str) -> dict:
    root = Path(repo).resolve()
    return {"repo": str(root), "detected": (root / "packages" / "topoaccess_prod").exists(), "status": "pass"}


def list_workspaces() -> list[dict]:
    rows: list[dict] = []
    for path in (WORKSPACE_STATE, LEGACY_WORKSPACE_STATE):
        if path.exists():
            rows.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
    return rows


def validate_workspace(profile: str) -> dict:
    matches = [w for w in list_workspaces() if w.get("profile") == profile]
    return {"profile": profile, "valid": bool(matches) or profile == "default", "status": "pass"}
