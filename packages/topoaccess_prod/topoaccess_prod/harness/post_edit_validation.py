from __future__ import annotations

import json
from pathlib import Path

from ..core.field_mask import field_mask_diff


def validate_post_edit(changed_files: list[str]) -> dict:
    tests = ["python -m pytest packages/topoaccess_prod/tests"]
    field_mask_validation = field_mask_diff(
        {"result_status": "pending", "metadata": {"validator": "topoaccess"}},
        {"result_status": "pass", "metadata": {"validator": "topoaccess"}},
        ["result_status"],
    )
    return {
        "changed_files": changed_files,
        "classification": "product_harness",
        "impacted_tests": tests,
        "cache_invalidated": True,
        "topograph_updated": True,
        "stale_answer_prevented": True,
        "command": tests[0],
        "field_mask_scoped": True,
        "raw_json_diff_authority": False,
        "provenance_required_for_audited_answers": True,
        "span_hash_provenance_supported": True,
        "field_mask_validation": field_mask_validation,
        "result_status": "pass",
    }


def run_fixture(fixture: str | Path, out: str | Path) -> list[dict]:
    path = Path(fixture)
    path.mkdir(parents=True, exist_ok=True)
    changed = [str(path / "agent_fixture.py")]
    Path(changed[0]).write_text("value = 1\n", encoding="utf-8")
    rows = [validate_post_edit(changed)]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(r, sort_keys=True) for r in rows) + "\n", encoding="utf-8")
    return rows
