from __future__ import annotations

import json
from pathlib import Path

from ..core.policies import route_for_category


def build_prompt_pack(task: str, mode: str = "standard", category: str = "change_planning") -> dict:
    tokens = {"minimal": 420, "standard": 760, "audit": 1120, "codex": 860, "claude": 900, "openclaw": 880}.get(mode, 760)
    return {
        "task": task,
        "mode": mode,
        "category": category,
        "repo_summary": "TopoAccess product package over stable V29 runtime wrappers.",
        "relevant_files": ["packages/topoaccess_prod/topoaccess_prod/cli/topoaccessctl.py"],
        "relevant_symbols": ["run_command", "route_for_category"],
        "tests": ["python -m pytest packages/topoaccess_prod/tests"],
        "commands": ["python packages/topoaccess_prod/scripts/topoaccessctl.py self-check --cache cache/topoaccess_v21"],
        "provenance": ["release/topoaccess_prod/release_manifest.json", "runs/topoaccess_prod/package_boundary.jsonl"],
        "constraints": ["Exact lookup remains tool-only", "Preferred model remains category-gated"],
        "risks": ["Do not import exploratory modules without justification"],
        "route_policy": route_for_category(category),
        "guidance": "Do not read irrelevant files; use this compact pack and provenance first.",
        "context_pack_tokens": tokens,
    }


def write_prompt_packs(tasks: list[str], out: str | Path) -> list[dict]:
    rows = [build_prompt_pack(task, mode=mode) for task in tasks for mode in ["minimal", "standard", "audit", "codex", "claude", "openclaw"]]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    return rows
