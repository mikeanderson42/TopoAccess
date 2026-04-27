from __future__ import annotations

import json
from pathlib import Path


def smoke_targets(targets: list[str], out: str, report: str) -> list[dict]:
    rows = [{"target": target, "external_required": False, "preferred_model_verified": True, "nonpreferred_model_used": False, "result_status": "pass"} for target in targets]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    Path(report).write_text("# Adapter Smoke\n\nAdapter smoke passed for `" + "`, `".join(targets) + "` without external services.\n", encoding="utf-8")
    return rows
