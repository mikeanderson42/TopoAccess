from __future__ import annotations

from pathlib import Path


def alias_script(profile: str = "default") -> str:
    return f"alias topoaccess='python packages/topoaccess_prod/scripts/topoaccessctl.py'\nalias topoaccess-agent='python packages/topoaccess_prod/scripts/topoaccess_agent.py --profile {profile}'\n"


def write_alias_script(path: str, profile: str = "default") -> dict:
    Path(path).write_text(alias_script(profile), encoding="utf-8")
    return {"path": path, "profile": profile, "result_status": "pass"}

