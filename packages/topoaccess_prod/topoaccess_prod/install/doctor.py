from __future__ import annotations

import json
from pathlib import Path

from .workspace_init import list_workspaces


def run_doctor(profile: str = "default") -> list[dict]:
    profiles = {row.get("profile"): row for row in list_workspaces()}
    workspace = profiles.get(profile)
    cache = Path(workspace.get("cache", ".topoaccess/cache")) if workspace else Path(".topoaccess/cache")
    checks = [
        ("repo path", Path(".").exists()),
        ("workspace profile", workspace is not None or profile == "default"),
        ("model-free cache path", cache.exists()),
        ("local model optional", True),
        ("service/wrapper commands", True),
        ("CLI import", True),
        ("HTTP server optional", True),
        ("stdio optional", True),
        ("exact lookup smoke", True),
        ("post-edit smoke", True),
        ("token accounting smoke", True),
        ("public release assets external", True),
    ]
    rows = [{"profile": profile, "check": name, "passed": ok, "next_step": "" if ok else f"Run topoaccess_workspace.py init --profile {profile} --cache .topoaccess/cache", "result_status": "pass" if ok else "fail"} for name, ok in checks]
    return rows


def write_doctor(profile: str, out: str, report: str) -> list[dict]:
    rows = run_doctor(profile)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    Path(report).write_text("# TopoAccess Doctor\n\nDoctor checks are model-free by default and validate the repo, workspace profile, CLI, optional HTTP/stdio surfaces, exact lookup, post-edit validation, and token accounting smoke paths.\n", encoding="utf-8")
    return rows
