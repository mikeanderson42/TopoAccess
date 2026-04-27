from __future__ import annotations

import json
from collections import defaultdict
from pathlib import Path

from .scenario_fixtures import MODES, build_dataset, write_dataset
from .workflow_scorer import TOPO_MODES, score_step, selection_score


def run_scenarios(
    dataset_path: str | Path,
    scenarios: int,
    fallback_scenarios: int,
    chunk_size: int,
    seed: int,
    modes: list[str] | None,
    out: str | Path,
    summary: str | Path,
    report: str | Path,
    resume: bool = False,
) -> list[dict]:
    target = scenarios if scenarios <= 2500 else min(scenarios, max(fallback_scenarios, 2500))
    dataset = _load_dataset(dataset_path)
    selected_modes = modes or MODES
    out_path = Path(out)
    existing = _load_rows(out_path) if resume else []
    start_scenario = len({r["scenario_id"] + ":" + r["mode"] for r in existing}) // max(1, len(selected_modes)) if existing else 0
    rows = list(existing)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    with out_path.open("a" if existing and resume else "w", encoding="utf-8") as stream:
        for scenario_index in range(start_scenario, target):
            scenario = dataset[scenario_index % len(dataset)]
            scenario_run_id = f"{scenario['scenario_id']}-{seed}-{scenario_index}"
            for mode in selected_modes:
                for step_idx, category in enumerate(scenario["categories"], start=1):
                    row = {
                        "run_id": "topoaccess_prod_v45",
                        "seed": seed,
                        "scenario_id": scenario_run_id,
                        "fixture_repo": scenario["fixture_repo"],
                        "workflow_type": scenario["workflow_type"],
                        "step_number": step_idx,
                        "total_steps": scenario["total_steps"],
                        "mode": mode,
                        "category": category,
                    }
                    row.update(score_step(scenario, mode, step_idx, category, seed + scenario_index))
                    stream.write(json.dumps(row, sort_keys=True) + "\n")
                    rows.append(row)
    write_scenario_summary(rows, summary, report)
    return rows


def build_dataset_file(fixtures: str | Path, out: str | Path, report: str | Path) -> list[dict]:
    return write_dataset(fixtures, out, report)


def write_scenario_summary(rows: list[dict], out: str | Path, report: str | Path | None = None, markdown: str | Path | None = None) -> dict:
    summary = summarize_scenarios(rows)
    Path(out).parent.mkdir(parents=True, exist_ok=True)
    Path(out).write_text(json.dumps(summary, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    if markdown:
        write_scenario_markdown(summary, markdown)
    if report:
        Path(report).write_text(_report_text(summary), encoding="utf-8")
    return summary


def summarize_scenarios(rows: list[dict]) -> dict:
    topo = [r for r in rows if r["mode"] in TOPO_MODES]
    workflows = defaultdict(list)
    modes = defaultdict(list)
    for row in rows:
        if row["mode"] in TOPO_MODES:
            workflows[row["workflow_type"]].append(row)
        modes[row["mode"]].append(row)
    scenario_ids = {r["scenario_id"] for r in rows}
    return {
        "scenario_workflows": len(scenario_ids),
        "steps": len(rows),
        "assisted_steps": len(topo),
        "average_token_savings": _mean([r["token_savings"] for r in topo]),
        "median_token_savings": _median([r["token_savings"] for r in topo]),
        "p10_token_savings": _percentile([r["token_savings"] for r in topo], 10),
        "p90_token_savings": _percentile([r["token_savings"] for r in topo], 90),
        "p50_latency_ms": _median([r["latency_ms"] for r in rows]),
        "p95_latency_ms": _percentile([r["latency_ms"] for r in rows], 95),
        "cache_hit_rate": _mean([1.0 if r["cache_hit"] else 0.0 for r in topo]),
        "average_cache_reuse_count": _mean([r["cache_reuse_count"] for r in topo]),
        "file_selection_accuracy": _mean([selection_score(r["files_selected"], r["expected_files"]) for r in topo]),
        "test_selection_recall": _mean([selection_score(r["tests_selected"], r["expected_tests"]) for r in topo]),
        "command_correctness": _mean([selection_score(r["commands_selected"], r["expected_commands"]) for r in topo]),
        "provenance_coverage": _mean([1.0 if r["provenance_count"] else 0.0 for r in topo]),
        "post_edit_validation_pass_rate": _mean([1.0 if r["post_edit_validation_passed"] else 0.0 for r in rows if r["category"] == "post_edit_validation"]),
        "assisted_post_edit_validation_pass_rate": _mean([1.0 if r["post_edit_validation_passed"] else 0.0 for r in topo if r["category"] == "post_edit_validation"]),
        "stale_cache_prevention_rate": _mean([1.0 if r["stale_cache_prevented"] else 0.0 for r in topo if r["category"] == "post_edit_validation"]),
        "hallucinated_file_count": sum(r["hallucinated_file_count"] for r in rows),
        "hallucinated_command_count": sum(r["hallucinated_command_count"] for r in rows),
        "topoaccess_hallucinated_file_count": sum(r["hallucinated_file_count"] for r in topo),
        "topoaccess_hallucinated_command_count": sum(r["hallucinated_command_count"] for r in topo),
        "unsupported_correct_rate": _mean([1.0 if r["unsupported_correct"] else 0.0 for r in rows if r["category"] in {"unsupported", "ambiguous", "prompt_injection"}]),
        "wrong_high_confidence": sum(r["wrong_high_confidence"] for r in rows),
        "unsupported_high_confidence": sum(r["unsupported_high_confidence"] for r in rows),
        "by_workflow": {k: _group_summary(v) for k, v in sorted(workflows.items())},
        "by_mode": {k: _group_summary(v) for k, v in sorted(modes.items())},
    }


def write_scenario_markdown(summary: dict, path: str | Path) -> None:
    lines = [
        "# TopoAccess Scenario Benchmark Summary",
        "",
        f"- Scenario workflows: `{summary['scenario_workflows']}`",
        f"- Steps: `{summary['steps']}`",
        f"- Average assisted token savings: `{summary['average_token_savings']:.4f}`",
        f"- Median assisted token savings: `{summary['median_token_savings']:.4f}`",
        f"- p50/p95 latency: `{summary['p50_latency_ms']:.1f} ms` / `{summary['p95_latency_ms']:.1f} ms`",
        f"- Cache hit rate: `{summary['cache_hit_rate']:.4f}`",
        f"- Post-edit validation pass rate, all modes: `{summary['post_edit_validation_pass_rate']:.4f}`",
        f"- Post-edit validation pass rate, assisted modes: `{summary['assisted_post_edit_validation_pass_rate']:.4f}`",
        f"- Wrong high-confidence: `{summary['wrong_high_confidence']}`",
        f"- Unsupported high-confidence: `{summary['unsupported_high_confidence']}`",
        "",
        "## Workflow Summary",
        "",
        "| Workflow | Steps | Avg Savings | p50 Latency ms |",
        "| --- | ---: | ---: | ---: |",
    ]
    for name, row in summary["by_workflow"].items():
        lines.append(f"| {name} | {row['steps']} | {row['average_token_savings']:.4f} | {row['p50_latency_ms']:.1f} |")
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")


def _group_summary(rows: list[dict]) -> dict:
    return {
        "steps": len(rows),
        "average_token_savings": _mean([r["token_savings"] for r in rows]),
        "median_token_savings": _median([r["token_savings"] for r in rows]),
        "p50_latency_ms": _median([r["latency_ms"] for r in rows]),
        "p95_latency_ms": _percentile([r["latency_ms"] for r in rows], 95),
    }


def _report_text(summary: dict) -> str:
    return (
        "# TopoAccess Scenario Benchmark\n\n"
        f"- Scenario workflows: `{summary['scenario_workflows']}`\n"
        f"- Steps: `{summary['steps']}`\n"
        f"- Average assisted token savings: `{summary['average_token_savings']:.4f}`\n"
        f"- Median assisted token savings: `{summary['median_token_savings']:.4f}`\n"
        f"- p50/p95 latency: `{summary['p50_latency_ms']:.1f} ms` / `{summary['p95_latency_ms']:.1f} ms`\n"
        f"- Wrong high-confidence: `{summary['wrong_high_confidence']}`\n"
        f"- Unsupported high-confidence: `{summary['unsupported_high_confidence']}`\n"
    )


def _load_dataset(path: str | Path) -> list[dict]:
    return [json.loads(line) for line in Path(path).read_text(encoding="utf-8").splitlines() if line.strip()]


def _load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _mean(values: list[float]) -> float:
    return sum(values) / len(values) if values else 0.0


def _median(values: list[float]) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    mid = len(ordered) // 2
    return ordered[mid] if len(ordered) % 2 else (ordered[mid - 1] + ordered[mid]) / 2


def _percentile(values: list[float], percentile: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    idx = round((len(ordered) - 1) * percentile / 100)
    return ordered[idx]
