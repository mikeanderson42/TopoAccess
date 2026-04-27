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


def mine_failures(input_path: str | Path | list[str], out: str | Path, report: str | Path) -> list[dict]:
    rows = _load_any(input_path)
    worst_savings = sorted([r for r in rows if "token_savings" in r], key=lambda r: r["token_savings"])[:25]
    slowest = sorted(rows, key=lambda r: r.get("latency_ms", 0), reverse=True)[:25]
    failures = [r for r in rows if r.get("result_status") != "pass"]
    hallucinations = [r for r in rows if r.get("hallucinated_file_count", 0) or r.get("hallucinated_command_count", 0)]
    topo_hallucinations = [r for r in hallucinations if _mode(r) in TOPOACCESS_MODES or r.get("cli_mode") == "topoaccess"]
    unsupported_failures = [
        r
        for r in rows
        if r.get("unsupported_high_confidence", 0)
        or (r.get("category") in {"unsupported", "ambiguous", "prompt_injection"} and r.get("unsupported_correct", True) is False)
    ]
    topo_unsupported_failures = [r for r in unsupported_failures if _mode(r) in TOPOACCESS_MODES or r.get("cli_mode") == "topoaccess"]
    weak_selection = [
        r
        for r in rows
        if min(r.get("file_selection_score", 1.0), r.get("test_selection_score", 1.0), r.get("command_selection_score", 1.0)) < 0.8
    ]
    mined = []
    for label, group in [
        ("lowest_token_savings", worst_savings),
        ("slowest_routes", slowest),
        ("explicit_failures", failures),
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
        "task_id": row.get("task_id", row.get("scenario_id", "")),
        "category": row.get("category", ""),
        "mode": _mode(row),
        "token_savings": row.get("token_savings"),
        "latency_ms": row.get("latency_ms"),
        "result_status": row.get("result_status"),
    }


def _mode(row: dict) -> str:
    return str(row.get("topoaccess_mode", row.get("mode", row.get("cli_mode", ""))))


def _load_any(input_path: str | Path | list[str]) -> list[dict]:
    if isinstance(input_path, list):
        rows: list[dict] = []
        for item in input_path:
            for path in sorted(Path().glob(str(item))):
                if path.name in {"audit.jsonl", "secret_scan.jsonl", "dogfood_preflight.jsonl"}:
                    continue
                rows.extend(json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip())
        return rows
    return load_rows(input_path)


def _report(rows: list[dict]) -> str:
    lines = ["# TopoAccess Failure Mining", ""]
    for row in rows:
        lines.append(f"- {row['kind']}: `{row['rows']}` rows")
    lines.extend(["", "No wrong high-confidence or unsupported high-confidence failures are expected in the deterministic public benchmark; any nonzero count should block public claims."])
    return "\n".join(lines) + "\n"
