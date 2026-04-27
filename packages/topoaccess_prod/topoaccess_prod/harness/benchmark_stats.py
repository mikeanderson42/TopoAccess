from __future__ import annotations

import json
import statistics
from collections import defaultdict
from pathlib import Path

TOPOACCESS_MODES = {
    "codex_style_with_topoaccess",
    "topoaccess_tool_only",
    "topoaccess_category_gated",
    "generic_agent_with_topoaccess",
    "http_tool_mode",
    "stdio_tool_mode",
}


def load_rows(path: str | Path) -> list[dict]:
    p = Path(path)
    if not p.exists():
        return []
    return [json.loads(line) for line in p.read_text(encoding="utf-8").splitlines() if line.strip()]


def summarize_rows(rows: list[dict]) -> dict:
    assisted = [r for r in rows if r["topoaccess_mode"] in TOPOACCESS_MODES]
    values = [r["token_savings"] for r in assisted]
    latencies = [r["latency_ms"] for r in assisted]
    all_latencies = [r["latency_ms"] for r in rows]
    by_category = _group(assisted, "category")
    by_mode = _group(rows, "topoaccess_mode")
    return {
        "rows": len(rows),
        "assisted_rows": len(assisted),
        "categories": sorted(by_category),
        "modes": sorted(by_mode),
        "average_token_savings": _mean(values),
        "median_token_savings": _median(values),
        "p10_token_savings": _percentile(values, 10),
        "p90_token_savings": _percentile(values, 90),
        "mean_token_savings_ci95": _mean_ci(values),
        "average_latency_ms": _mean(all_latencies),
        "p50_latency_ms": _median(all_latencies),
        "p95_latency_ms": _percentile(all_latencies, 95),
        "assisted_p50_latency_ms": _median(latencies),
        "assisted_p95_latency_ms": _percentile(latencies, 95),
        "file_selection_score": _mean([r["file_selection_score"] for r in assisted]),
        "test_selection_score": _mean([r["test_selection_score"] for r in assisted]),
        "command_selection_score": _mean([r["command_selection_score"] for r in assisted]),
        "provenance_coverage": _mean([1.0 if r["provenance_count"] > 0 else 0.0 for r in assisted]),
        "unsupported_correct_rate": _mean([1.0 if r["unsupported_correct"] else 0.0 for r in rows if r["category"] in {"unsupported", "ambiguous", "prompt_injection"}]),
        "hallucinated_file_count": sum(r["hallucinated_file_count"] for r in rows),
        "hallucinated_command_count": sum(r["hallucinated_command_count"] for r in rows),
        "wrong_high_confidence": sum(r["wrong_high_confidence"] for r in rows),
        "unsupported_high_confidence": sum(r["unsupported_high_confidence"] for r in rows),
        "model_invocation_rate": _mean([1.0 if r["model_invoked"] else 0.0 for r in rows]),
        "by_category": {k: _summary_for(v) for k, v in sorted(by_category.items())},
        "by_mode": {k: _summary_for(v) for k, v in sorted(by_mode.items())},
    }


def write_summary(rows: list[dict], out: str | Path, markdown: str | Path | None = None) -> dict:
    summary = summarize_rows(rows)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if markdown:
        write_summary_markdown(summary, markdown)
    return summary


def write_summary_markdown(summary: dict, path: str | Path) -> None:
    lines = [
        "# TopoAccess Benchmark Summary",
        "",
        f"- Rows: `{summary['rows']}`",
        f"- Assisted rows: `{summary['assisted_rows']}`",
        f"- Average assisted token savings: `{summary['average_token_savings']:.4f}`",
        f"- Median assisted token savings: `{summary['median_token_savings']:.4f}`",
        f"- p10/p90 assisted token savings: `{summary['p10_token_savings']:.4f}` / `{summary['p90_token_savings']:.4f}`",
        f"- p50/p95 latency across all modes: `{summary['p50_latency_ms']:.1f} ms` / `{summary['p95_latency_ms']:.1f} ms`",
        f"- Wrong high-confidence: `{summary['wrong_high_confidence']}`",
        f"- Unsupported high-confidence: `{summary['unsupported_high_confidence']}`",
        "",
        "## Category Summary",
        "",
        "| Category | Rows | Avg Savings | p50 Latency ms | Provenance |",
        "| --- | ---: | ---: | ---: | ---: |",
    ]
    for category, row in summary["by_category"].items():
        lines.append(f"| {category} | {row['rows']} | {row['average_token_savings']:.4f} | {row['p50_latency_ms']:.1f} | {row['provenance_coverage']:.3f} |")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _group(rows: list[dict], key: str) -> dict[str, list[dict]]:
    grouped: dict[str, list[dict]] = defaultdict(list)
    for row in rows:
        grouped[row[key]].append(row)
    return grouped


def _summary_for(rows: list[dict]) -> dict:
    return {
        "rows": len(rows),
        "average_token_savings": _mean([r["token_savings"] for r in rows]),
        "median_token_savings": _median([r["token_savings"] for r in rows]),
        "p50_latency_ms": _median([r["latency_ms"] for r in rows]),
        "p95_latency_ms": _percentile([r["latency_ms"] for r in rows], 95),
        "file_selection_score": _mean([r["file_selection_score"] for r in rows]),
        "test_selection_score": _mean([r["test_selection_score"] for r in rows]),
        "command_selection_score": _mean([r["command_selection_score"] for r in rows]),
        "provenance_coverage": _mean([1.0 if r["provenance_count"] > 0 else 0.0 for r in rows]),
    }


def _mean(values: list[float]) -> float:
    return float(sum(values) / len(values)) if values else 0.0


def _median(values: list[float]) -> float:
    return float(statistics.median(values)) if values else 0.0


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = round((len(ordered) - 1) * percentile / 100)
    return float(ordered[idx])


def _mean_ci(values: list[float]) -> list[float]:
    if len(values) < 2:
        avg = _mean(values)
        return [avg, avg]
    avg = _mean(values)
    stdev = statistics.pstdev(values)
    margin = 1.96 * stdev / (len(values) ** 0.5)
    return [max(0.0, avg - margin), min(1.0, avg + margin)]
