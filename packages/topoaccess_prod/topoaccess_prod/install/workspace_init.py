from __future__ import annotations

import json
from pathlib import Path


def init_workspace(profile: str, repo: str, cache: str, preferred_search: str) -> dict:
    row = {
        "profile": profile,
        "repo": str(Path(repo).resolve()),
        "cache": cache,
        "preferred_search": preferred_search,
        "release": "release/topoaccess_prod",
        "status": "pass",
    }
    Path("runs/topoaccess_prod_v32").mkdir(parents=True, exist_ok=True)
    with Path("runs/topoaccess_prod_v32/workspaces.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, sort_keys=True) + "\n")
    return row


def detect_workspace(repo: str) -> dict:
    root = Path(repo).resolve()
    return {"repo": str(root), "detected": (root / "packages" / "topoaccess_prod").exists(), "status": "pass"}


def list_workspaces() -> list[dict]:
    path = Path("runs/topoaccess_prod_v32/workspaces.jsonl")
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_workspace(profile: str) -> dict:
    matches = [w for w in list_workspaces() if w.get("profile") == profile]
    return {"profile": profile, "valid": bool(matches) or profile == "default", "status": "pass"}
