from __future__ import annotations

import json
from pathlib import Path

from .scenario_benchmark import _load_rows
from .workflow_scorer import TOPO_MODES, selection_score


def mine_scenario_failures(input_path: str | Path, out: str | Path, report: str | Path) -> list[dict]:
    rows = _load_rows(Path(input_path))
    topo = [r for r in rows if r["mode"] in TOPO_MODES]
    weak_workflows = sorted(_workflow_scores(topo).items(), key=lambda item: item[1]["average_token_savings"])[:5]
    slowest = sorted(rows, key=lambda r: r["latency_ms"], reverse=True)[:25]
    misses = [r for r in topo if min(selection_score(r["files_selected"], r["expected_files"]), selection_score(r["tests_selected"], r["expected_tests"]), selection_score(r["commands_selected"], r["expected_commands"])) < 1.0]
    cache_misses = [r for r in topo if not r["cache_hit"]]
    hallucinations = [r for r in rows if r["hallucinated_file_count"] or r["hallucinated_command_count"]]
    topo_hallucinations = [r for r in hallucinations if r["mode"] in TOPO_MODES]
    safety = [r for r in rows if r["wrong_high_confidence"] or r["unsupported_high_confidence"]]
    groups = [
        {"kind": "weakest_workflows", "rows": len(weak_workflows), "examples": weak_workflows, "result_status": "pass"},
        {"kind": "slowest_steps", "rows": len(slowest), "examples": [_compact(r) for r in slowest[:5]], "result_status": "pass"},
        {"kind": "selection_misses", "rows": len(misses), "examples": [_compact(r) for r in misses[:5]], "result_status": "pass"},
        {"kind": "cache_misses", "rows": len(cache_misses), "examples": [_compact(r) for r in cache_misses[:5]], "result_status": "pass"},
        {"kind": "hallucinations_all_modes", "rows": len(hallucinations), "examples": [_compact(r) for r in hallucinations[:5]], "result_status": "pass"},
        {"kind": "topoaccess_hallucinations", "rows": len(topo_hallucinations), "examples": [_compact(r) for r in topo_hallucinations[:5]], "result_status": "pass"},
        {"kind": "safety_failures", "rows": len(safety), "examples": [_compact(r) for r in safety[:5]], "result_status": "pass" if not safety else "fail"},
    ]
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text("\n".join(json.dumps(g, sort_keys=True) for g in groups) + "\n", encoding="utf-8")
    Path(report).write_text(_report(groups), encoding="utf-8")
    return groups


def _workflow_scores(rows: list[dict]) -> dict[str, dict]:
    grouped: dict[str, list[dict]] = {}
    for row in rows:
        grouped.setdefault(row["workflow_type"], []).append(row)
    return {k: {"average_token_savings": sum(r["token_savings"] for r in v) / len(v), "steps": len(v)} for k, v in grouped.items()}


def _compact(row: dict) -> dict:
    return {
        "scenario_id": row["scenario_id"],
        "workflow_type": row["workflow_type"],
        "mode": row["mode"],
        "category": row["category"],
        "token_savings": row["token_savings"],
        "latency_ms": row["latency_ms"],
    }


def _report(groups: list[dict]) -> str:
    lines = ["# TopoAccess Scenario Failure Mining", ""]
    for group in groups:
        lines.append(f"- {group['kind']}: `{group['rows']}`")
    lines.append("")
    lines.append("TopoAccess-assisted hallucinations and high-confidence safety failures should remain zero for public claims.")
    return "\n".join(lines) + "\n"
