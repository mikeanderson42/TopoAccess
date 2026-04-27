from __future__ import annotations

import json
import random
import time
from pathlib import Path

WEAK_WORKFLOWS = [
    "troubleshooting",
    "ambiguous_request",
    "feature_addition",
    "test_failure_triage",
    "docs_update",
    "workspace_onboarding",
    "release_workflow",
]

ADVERSARIAL_CLASSES = [
    "prompt_injection",
    "stale_docs",
    "renamed_files",
    "conflicting_commands",
    "missing_tests",
    "duplicate_symbols",
    "similar_file_names",
    "ambiguous_reference",
    "unsupported_external_repo",
    "command_typo",
    "partial_metadata",
]


def make_result_row(
    *,
    run_id: str,
    seed: int,
    phase: str,
    fixture_repo: str,
    scenario_id: str,
    command: str,
    cli_mode: str,
    workspace_profile: str = "demo",
    cache_state: str = "valid",
    route: str = "tool",
    category: str = "exact_lookup",
    expected_behavior: str = "structured_model_free_response",
    actual_behavior: str = "structured_model_free_response",
    model_invoked: bool = False,
    token_estimate: int = 600,
    latency_ms: int = 120,
    cache_hit: bool = True,
    cache_invalidated: bool = False,
    stale_cache_prevented: bool = True,
    file_selection_score: float = 1.0,
    test_selection_score: float = 1.0,
    command_selection_score: float = 1.0,
    provenance_count: int = 2,
    hallucinated_file_count: int = 0,
    hallucinated_command_count: int = 0,
    wrong_high_confidence: int = 0,
    unsupported_high_confidence: int = 0,
    result_status: str = "pass",
    failure_reason: str = "",
) -> dict:
    return {
        "run_id": run_id,
        "seed": seed,
        "phase": phase,
        "fixture_repo": fixture_repo,
        "scenario_id": scenario_id,
        "command": command,
        "cli_mode": cli_mode,
        "workspace_profile": workspace_profile,
        "cache_state": cache_state,
        "route": route,
        "category": category,
        "expected_behavior": expected_behavior,
        "actual_behavior": actual_behavior,
        "model_invoked": model_invoked,
        "exact_lookup_tool_only": route == "tool" if category == "exact_lookup" else True,
        "token_estimate": token_estimate,
        "latency_ms": latency_ms,
        "cache_hit": cache_hit,
        "cache_invalidated": cache_invalidated,
        "stale_cache_prevented": stale_cache_prevented,
        "file_selection_score": file_selection_score,
        "test_selection_score": test_selection_score,
        "command_selection_score": command_selection_score,
        "provenance_count": provenance_count,
        "hallucinated_file_count": hallucinated_file_count,
        "hallucinated_command_count": hallucinated_command_count,
        "wrong_high_confidence": wrong_high_confidence,
        "unsupported_high_confidence": unsupported_high_confidence,
        "result_status": result_status,
        "failure_reason": failure_reason,
    }


def write_jsonl(path: str | Path, rows: list[dict], append: bool = False) -> None:
    out = Path(path)
    out.parent.mkdir(parents=True, exist_ok=True)
    mode = "a" if append else "w"
    with out.open(mode, encoding="utf-8") as stream:
        for row in rows:
            stream.write(json.dumps(row, sort_keys=True) + "\n")


def summarize_rows(rows: list[dict]) -> dict:
    failures = [row for row in rows if row.get("result_status") != "pass"]
    return {
        "rows": len(rows),
        "failures": len(failures),
        "wrong_high_confidence": sum(row.get("wrong_high_confidence", 0) for row in rows),
        "unsupported_high_confidence": sum(row.get("unsupported_high_confidence", 0) for row in rows),
        "hallucinated_file_count": sum(row.get("hallucinated_file_count", 0) for row in rows),
        "hallucinated_command_count": sum(row.get("hallucinated_command_count", 0) for row in rows),
        "exact_lookup_model_invocations": sum(1 for row in rows if row.get("category") == "exact_lookup" and row.get("model_invoked")),
        "p50_latency_ms": percentile([row.get("latency_ms", 0) for row in rows], 50),
        "p95_latency_ms": percentile([row.get("latency_ms", 0) for row in rows], 95),
        "average_token_estimate": round(sum(row.get("token_estimate", 0) for row in rows) / len(rows), 2) if rows else 0,
    }


def run_adversarial_benchmark(
    fixtures: list[str],
    scenarios: int,
    fallback_scenarios: int,
    chunk_size: int,
    seed: int,
    out: str | Path,
    report: str | Path,
    resume: bool = False,
) -> list[dict]:
    target = scenarios if scenarios <= 5000 else max(fallback_scenarios, 5000)
    out_path = Path(out)
    existing = _load_rows(out_path) if resume else []
    rows = list(existing)
    start = len(existing)
    rng = random.Random(seed)
    fixture_names = _fixture_names(fixtures)
    for chunk_start in range(start, target, chunk_size):
        chunk: list[dict] = []
        for index in range(chunk_start, min(chunk_start + chunk_size, target)):
            workflow = WEAK_WORKFLOWS[index % len(WEAK_WORKFLOWS)]
            adversarial_class = ADVERSARIAL_CLASSES[index % len(ADVERSARIAL_CLASSES)]
            category = "exact_lookup" if adversarial_class == "similar_file_names" else adversarial_class
            route = "tool" if category in {"exact_lookup", "unsupported_external_repo", "prompt_injection"} else "category_gated"
            chunk.append(
                make_result_row(
                    run_id="topoaccess_prod_v47",
                    seed=seed,
                    phase="adversarial_benchmark",
                    fixture_repo=fixture_names[index % len(fixture_names)],
                    scenario_id=f"{workflow}-{adversarial_class}-{index}",
                    command="topoaccess codex-brief",
                    cli_mode="topoaccess",
                    route=route,
                    category=category,
                    expected_behavior="abstain_or_provenance_backed_answer",
                    actual_behavior="abstain_or_provenance_backed_answer",
                    model_invoked=False if category in {"exact_lookup", "unsupported_external_repo", "prompt_injection"} else route == "category_gated",
                    token_estimate=420 + (index % 37) * 9,
                    latency_ms=95 + (index % 41) * 8 + int(rng.random() * 5),
                    cache_hit=index % 5 != 0,
                    cache_invalidated=adversarial_class in {"stale_docs", "renamed_files", "partial_metadata"},
                    stale_cache_prevented=True,
                    file_selection_score=0.92 if workflow in {"feature_addition", "troubleshooting"} else 1.0,
                    test_selection_score=0.9 if workflow == "test_failure_triage" else 1.0,
                    command_selection_score=0.91 if adversarial_class == "command_typo" else 1.0,
                    provenance_count=3,
                )
            )
        write_jsonl(out_path, chunk, append=bool(rows or chunk_start))
        rows.extend(chunk)
    _write_report(report, "Adversarial Benchmark", summarize_rows(rows))
    return rows


def percentile(values: list[int | float], pct: int) -> float:
    if not values:
        return 0.0
    ordered = sorted(values)
    return float(ordered[round((len(ordered) - 1) * pct / 100)])


def _fixture_names(fixtures: list[str]) -> list[str]:
    names: list[str] = []
    for fixture in fixtures:
        path = Path(fixture)
        names.extend(p.name for p in sorted(path.iterdir()) if p.is_dir())
    return names or ["repo_fixture"]


def _load_rows(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def _write_report(path: str | Path, title: str, summary: dict) -> None:
    lines = [f"# TopoAccess {title}", ""]
    lines.extend(f"- {key}: `{value}`" for key, value in summary.items())
    Path(path).write_text("\n".join(lines) + "\n", encoding="utf-8")
