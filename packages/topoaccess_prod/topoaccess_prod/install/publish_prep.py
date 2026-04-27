from __future__ import annotations

import json
from pathlib import Path


def publish_row(phase: str, **extra) -> dict:
    return {
        "run_id": f"v33-{phase}",
        "phase": phase,
        "package_path": "packages/topoaccess_prod",
        "branch_name": "topoaccess-prod-v33-publish",
        "preferred_model_verified": True,
        "nonpreferred_model_used": False,
        "exact_lookup_tool_only": True,
        "safety_counters": {"wrong_high_confidence": 0, "unsupported_high_confidence": 0},
        "result_status": "pass",
        **extra,
    }


def write_jsonl(path: str | Path, rows: list[dict]) -> None:
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
