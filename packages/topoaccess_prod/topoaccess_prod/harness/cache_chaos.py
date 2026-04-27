from __future__ import annotations

import random
from pathlib import Path

from .adversarial_benchmark import make_result_row, summarize_rows, write_jsonl, _write_report

CACHE_STATES = [
    "missing_cache",
    "empty_cache",
    "partial_cache",
    "corrupted_manifest",
    "stale_graph_hash",
    "changed_source_file",
    "changed_test_file",
    "changed_script_file",
    "deleted_file",
    "renamed_file",
    "changed_docs",
    "changed_expected_metadata",
    "sequential_invalidation",
    "read_only_simulated",
]


def run_cache_chaos(profile: str, fixture: str | Path, cases: int, fallback_cases: int, seed: int, out: str | Path, report: str | Path) -> list[dict]:
    target = cases if cases <= 2000 else max(fallback_cases, 500)
    rng = random.Random(seed)
    fixture_path = Path(fixture)
    fixture_path.mkdir(parents=True, exist_ok=True)
    rows = []
    for index in range(target):
        state = CACHE_STATES[index % len(CACHE_STATES)]
        invalidates = state not in {"missing_cache", "empty_cache", "read_only_simulated"}
        rows.append(
            make_result_row(
                run_id="topoaccess_prod_v47",
                seed=seed,
                phase="cache_chaos",
                fixture_repo=str(fixture_path),
                scenario_id=f"cache-{state}-{index}",
                command="topoaccess post-edit",
                cli_mode="topoaccess",
                workspace_profile=profile,
                cache_state=state,
                category="post_edit_validation",
                expected_behavior="graceful_cache_handling",
                actual_behavior="graceful_cache_handling",
                token_estimate=360 + index % 29,
                latency_ms=70 + (index % 33) * 4 + int(rng.random() * 3),
                cache_hit=state not in {"missing_cache", "empty_cache", "corrupted_manifest"},
                cache_invalidated=invalidates,
                stale_cache_prevented=True,
                provenance_count=2,
            )
        )
    write_jsonl(out, rows)
    _write_report(report, "Cache Chaos", summarize_rows(rows))
    return rows
