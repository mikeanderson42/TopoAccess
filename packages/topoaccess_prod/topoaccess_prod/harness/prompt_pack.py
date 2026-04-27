from __future__ import annotations

import json
from pathlib import Path

from ..core.policies import route_for_category
from ..core.provenance import make_span_provenance, verify_provenance_entries


def build_prompt_pack(task: str, mode: str = "standard", category: str = "change_planning") -> dict:
    tokens = {"minimal": 420, "standard": 760, "audit": 1120, "codex": 860, "claude": 900, "openclaw": 880}.get(mode, 760)
    relevant_files = ["packages/topoaccess_prod/topoaccess_prod/cli/topoaccessctl.py"]
    provenance = ["release/topoaccess_prod/release_manifest.json", "runs/topoaccess_prod/package_boundary.jsonl"]
    provenance_entries = _provenance_entries_for_files(relevant_files)
    provenance_verification = verify_provenance_entries(provenance_entries, require_span_hash=True)
    return {
        "task": task,
        "mode": mode,
        "category": category,
        "repo_summary": "TopoAccess product package over stable V29 runtime wrappers.",
        "relevant_files": relevant_files,
        "relevant_symbols": ["run_command", "route_for_category"],
        "tests": ["python -m pytest packages/topoaccess_prod/tests"],
        "commands": ["python packages/topoaccess_prod/scripts/topoaccessctl.py self-check --cache cache/topoaccess_v21"],
        "provenance": provenance,
        "provenance_entries": provenance_entries,
        "provenance_verified": provenance_verification["result_status"] == "pass",
        "provenance_verification": provenance_verification,
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


def _provenance_entries_for_files(files: list[str]) -> list[dict]:
    entries = []
    for source in files:
        path = Path(source)
        if not path.exists():
            entries.append({"source_uri": source, "verified": False, "reason": "source file not found"})
            continue
        line_count = len(path.read_text(encoding="utf-8").splitlines())
        end_line = min(max(line_count, 1), 20)
        try:
            entries.append(make_span_provenance(source, 1, end_line))
        except Exception as exc:  # noqa: BLE001 - prompt packs should report unverifiable sources.
            entries.append({"source_uri": source, "verified": False, "reason": str(exc)})
    return entries
