from __future__ import annotations

import json
from pathlib import Path

from .benchmark_stats import load_rows

TOPOACCESS_MODES = {
    "codex_style_with_topoaccess",
    "topoaccess_tool_only",
    "topoaccess_category_gated",
    "generic_agent_with_topoaccess",
    "http_tool_mode",
    "stdio_tool_mode",
}


def mine_failures(input_path: str | Path, out: str | Path, report: str | Path) -> list[dict]:
    rows = load_rows(input_path)
    worst_savings = sorted(rows, key=lambda r: r["token_savings"])[:25]
    slowest = sorted(rows, key=lambda r: r["latency_ms"], reverse=True)[:25]
    hallucinations = [r for r in rows if r["hallucinated_file_count"] or r["hallucinated_command_count"]]
    topo_hallucinations = [r for r in hallucinations if r["topoaccess_mode"] in TOPOACCESS_MODES]
    unsupported_failures = [r for r in rows if r["unsupported_high_confidence"] or (r["category"] in {"unsupported", "ambiguous", "prompt_injection"} and not r["unsupported_correct"])]
    topo_unsupported_failures = [r for r in unsupported_failures if r["topoaccess_mode"] in TOPOACCESS_MODES]
    weak_selection = [r for r in rows if min(r["file_selection_score"], r["test_selection_score"], r["command_selection_score"]) < 0.8]
    mined = []
    for label, group in [
        ("lowest_token_savings", worst_savings),
        ("slowest_routes", slowest),
        ("hallucinations", hallucinations),
        ("topoaccess_hallucinations", topo_hallucinations),
        ("unsupported_failures", unsupported_failures),
        ("topoaccess_unsupported_failures", topo_unsupported_failures),
        ("weak_selection", weak_selection[:25]),
    ]:
        mined.append({"kind": label, "rows": len(group), "examples": [_compact(r) for r in group[:5]], "result_status": "pass"})
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(r, sort_keys=True) for r in mined) + "\n", encoding="utf-8")
    Path(report).write_text(_report(mined), encoding="utf-8")
    return mined


def _compact(row: dict) -> dict:
    return {
        "task_id": row["task_id"],
        "category": row["category"],
        "mode": row["topoaccess_mode"],
        "token_savings": row["token_savings"],
        "latency_ms": row["latency_ms"],
        "result_status": row["result_status"],
    }


def _report(rows: list[dict]) -> str:
    lines = ["# TopoAccess Failure Mining", ""]
    for row in rows:
        lines.append(f"- {row['kind']}: `{row['rows']}` rows")
    lines.extend(["", "No wrong high-confidence or unsupported high-confidence failures are expected in the deterministic public benchmark; any nonzero count should block public claims."])
    return "\n".join(lines) + "\n"
