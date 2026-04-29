from __future__ import annotations

import json
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

from .scenario_fixtures import MODES, build_dataset, write_dataset
from .streaming_stats import BenchmarkRunResult, NumericSeries, iter_jsonl
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
) -> BenchmarkRunResult:
    target = scenarios if scenarios <= 2500 else min(scenarios, max(fallback_scenarios, 2500))
    dataset = list(iter_dataset(dataset_path))
    if not dataset:
        raise ValueError(f"scenario dataset is empty: {dataset_path}")
    selected_modes = modes or MODES
    out_path = Path(out)
    stats = ScenarioStats()
    retained_rows: list[dict] | None = [] if target <= 500 else None
    existing_pairs: set[str] = set()
    if resume:
        for row in iter_jsonl(out_path):
            stats.add(row)
            existing_pairs.add(row["scenario_id"] + ":" + row["mode"])
            if retained_rows is not None:
                retained_rows.append(row)
    start_scenario = len(existing_pairs) // max(1, len(selected_modes)) if existing_pairs else 0
    out_path.parent.mkdir(parents=True, exist_ok=True)
    chunk_rows: list[dict] = []
    chunk_base = out_path.parent / "scenario_chunks"
    with out_path.open("a" if existing_pairs and resume else "w", encoding="utf-8") as stream:
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
                    stats.add(row)
                    if retained_rows is not None:
                        retained_rows.append(row)
                    chunk_rows.append(row)
                    if len(chunk_rows) >= chunk_size:
                        chunk_base.mkdir(parents=True, exist_ok=True)
                        _write_rows(chunk_rows, chunk_base / f"chunk_{scenario_index + 1:06d}.jsonl")
                        chunk_rows = []
    if chunk_rows and target > 500:
        chunk_base.mkdir(parents=True, exist_ok=True)
        _write_rows(chunk_rows, chunk_base / f"chunk_{target:06d}.jsonl")
    write_scenario_summary(stats, summary, report)
    return BenchmarkRunResult(row_count=stats.steps, rows=retained_rows)


def build_dataset_file(fixtures: str | Path, out: str | Path, report: str | Path) -> list[dict]:
    return write_dataset(fixtures, out, report)


def write_scenario_summary(rows: list[dict] | "ScenarioStats", out: str | Path, report: str | Path | None = None, markdown: str | Path | None = None) -> dict:
    summary = rows.summary() if isinstance(rows, ScenarioStats) else summarize_scenarios(rows)
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
    return list(iter_dataset(path))


def _load_rows(path: Path) -> list[dict]:
    return list(iter_jsonl(path))


def iter_dataset(path: str | Path):
    yield from iter_jsonl(path)


def _write_rows(rows: list[dict], path: Path) -> None:
    path.write_text("\n".join(json.dumps(row, sort_keys=True) for row in rows) + "\n", encoding="utf-8")


@dataclass
class ScenarioGroupStats:
    steps: int = 0
    token_savings: NumericSeries = field(default_factory=NumericSeries)
    latency_ms: NumericSeries = field(default_factory=NumericSeries)

    def add(self, row: dict) -> None:
        self.steps += 1
        self.token_savings.add(row.get("token_savings", 0.0))
        self.latency_ms.add(row.get("latency_ms", 0.0))

    def summary(self) -> dict:
        return {
            "steps": self.steps,
            "average_token_savings": self.token_savings.mean(),
            "median_token_savings": self.token_savings.median(),
            "p50_latency_ms": self.latency_ms.median(),
            "p95_latency_ms": self.latency_ms.percentile(95),
        }


@dataclass
class ScenarioStats:
    scenario_ids: set[str] = field(default_factory=set)
    steps: int = 0
    assisted_steps: int = 0
    assisted_token_savings: NumericSeries = field(default_factory=NumericSeries)
    assisted_latency_ms: NumericSeries = field(default_factory=NumericSeries)
    all_latency_ms: NumericSeries = field(default_factory=NumericSeries)
    cache_hits: int = 0
    cache_reuse_count: int = 0
    file_score: NumericSeries = field(default_factory=NumericSeries)
    test_score: NumericSeries = field(default_factory=NumericSeries)
    command_score: NumericSeries = field(default_factory=NumericSeries)
    provenance_hits: int = 0
    post_edit_rows: int = 0
    post_edit_passes: int = 0
    assisted_post_edit_rows: int = 0
    assisted_post_edit_passes: int = 0
    stale_cache_rows: int = 0
    stale_cache_prevented: int = 0
    hallucinated_file_count: int = 0
    hallucinated_command_count: int = 0
    topoaccess_hallucinated_file_count: int = 0
    topoaccess_hallucinated_command_count: int = 0
    unsupported_rows: int = 0
    unsupported_correct: int = 0
    wrong_high_confidence: int = 0
    unsupported_high_confidence: int = 0
    by_workflow: dict[str, ScenarioGroupStats] = field(default_factory=dict)
    by_mode: dict[str, ScenarioGroupStats] = field(default_factory=dict)

    def add(self, row: dict) -> None:
        self.scenario_ids.add(row["scenario_id"])
        self.steps += 1
        mode = row["mode"]
        assisted = mode in TOPO_MODES
        category = row["category"]
        self.all_latency_ms.add(row.get("latency_ms", 0.0))
        self.by_mode.setdefault(mode, ScenarioGroupStats()).add(row)
        if assisted:
            self.assisted_steps += 1
            self.assisted_token_savings.add(row.get("token_savings", 0.0))
            self.assisted_latency_ms.add(row.get("latency_ms", 0.0))
            self.cache_hits += 1 if row.get("cache_hit") else 0
            self.cache_reuse_count += int(row.get("cache_reuse_count", 0))
            self.file_score.add(selection_score(row.get("files_selected", []), row.get("expected_files", [])))
            self.test_score.add(selection_score(row.get("tests_selected", []), row.get("expected_tests", [])))
            self.command_score.add(selection_score(row.get("commands_selected", []), row.get("expected_commands", [])))
            if row.get("provenance_count"):
                self.provenance_hits += 1
            self.by_workflow.setdefault(row["workflow_type"], ScenarioGroupStats()).add(row)
            self.topoaccess_hallucinated_file_count += int(row.get("hallucinated_file_count", 0))
            self.topoaccess_hallucinated_command_count += int(row.get("hallucinated_command_count", 0))
            if category == "post_edit_validation":
                self.assisted_post_edit_rows += 1
                if row.get("post_edit_validation_passed"):
                    self.assisted_post_edit_passes += 1
                self.stale_cache_rows += 1
                if row.get("stale_cache_prevented"):
                    self.stale_cache_prevented += 1
        if category == "post_edit_validation":
            self.post_edit_rows += 1
            if row.get("post_edit_validation_passed"):
                self.post_edit_passes += 1
        if category in {"unsupported", "ambiguous", "prompt_injection"}:
            self.unsupported_rows += 1
            if row.get("unsupported_correct"):
                self.unsupported_correct += 1
        self.hallucinated_file_count += int(row.get("hallucinated_file_count", 0))
        self.hallucinated_command_count += int(row.get("hallucinated_command_count", 0))
        self.wrong_high_confidence += int(row.get("wrong_high_confidence", 0))
        self.unsupported_high_confidence += int(row.get("unsupported_high_confidence", 0))

    def summary(self) -> dict:
        return {
            "scenario_workflows": len(self.scenario_ids),
            "steps": self.steps,
            "assisted_steps": self.assisted_steps,
            "average_token_savings": self.assisted_token_savings.mean(),
            "median_token_savings": self.assisted_token_savings.median(),
            "p10_token_savings": self.assisted_token_savings.percentile(10),
            "p90_token_savings": self.assisted_token_savings.percentile(90),
            "p50_latency_ms": self.all_latency_ms.median(),
            "p95_latency_ms": self.all_latency_ms.percentile(95),
            "cache_hit_rate": self.cache_hits / self.assisted_steps if self.assisted_steps else 0.0,
            "average_cache_reuse_count": self.cache_reuse_count / self.assisted_steps if self.assisted_steps else 0.0,
            "file_selection_accuracy": self.file_score.mean(),
            "test_selection_recall": self.test_score.mean(),
            "command_correctness": self.command_score.mean(),
            "provenance_coverage": self.provenance_hits / self.assisted_steps if self.assisted_steps else 0.0,
            "post_edit_validation_pass_rate": self.post_edit_passes / self.post_edit_rows if self.post_edit_rows else 0.0,
            "assisted_post_edit_validation_pass_rate": self.assisted_post_edit_passes / self.assisted_post_edit_rows if self.assisted_post_edit_rows else 0.0,
            "stale_cache_prevention_rate": self.stale_cache_prevented / self.stale_cache_rows if self.stale_cache_rows else 0.0,
            "hallucinated_file_count": self.hallucinated_file_count,
            "hallucinated_command_count": self.hallucinated_command_count,
            "topoaccess_hallucinated_file_count": self.topoaccess_hallucinated_file_count,
            "topoaccess_hallucinated_command_count": self.topoaccess_hallucinated_command_count,
            "unsupported_correct_rate": self.unsupported_correct / self.unsupported_rows if self.unsupported_rows else 0.0,
            "wrong_high_confidence": self.wrong_high_confidence,
            "unsupported_high_confidence": self.unsupported_high_confidence,
            "by_workflow": {k: v.summary() for k, v in sorted(self.by_workflow.items())},
            "by_mode": {k: v.summary() for k, v in sorted(self.by_mode.items())},
        }


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
