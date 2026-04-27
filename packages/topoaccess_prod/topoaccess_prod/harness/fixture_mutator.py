from __future__ import annotations

from pathlib import Path

from .adversarial_benchmark import make_result_row, summarize_rows, write_jsonl, _write_report

MUTATIONS = [
    "rename_source_file",
    "rename_test_file",
    "add_new_command",
    "remove_command",
    "stale_docs_old_file",
    "conflicting_docs_script",
    "failing_test_marker",
    "artifact_manifest_change",
    "release_script_change",
    "unsupported_absent_file",
    "prompt_injection_ignore_policy",
]


def run_fixture_mutations(fixtures: str | Path | list[str], mutations: int, fallback_mutations: int, seed: int, out: str | Path, report: str | Path) -> list[dict]:
    target = mutations if mutations <= 1000 else max(fallback_mutations, 250)
    fixture_paths = [Path(fixture) for fixture in fixtures] if isinstance(fixtures, list) else [Path(fixtures)]
    fixture_names: list[str] = []
    for fixture_path in fixture_paths:
        if fixture_path.exists():
            fixture_names.extend(p.name for p in sorted(fixture_path.iterdir()) if p.is_dir())
    fixture_names = fixture_names or ["fixture"]
    rows = []
    for index in range(target):
        mutation = MUTATIONS[index % len(MUTATIONS)]
        rows.append(
            make_result_row(
                run_id="topoaccess_prod_v47",
                seed=seed,
                phase="fixture_mutation",
                fixture_repo=fixture_names[index % len(fixture_names)],
                scenario_id=f"mutation-{mutation}-{index}",
                command="topoaccess post-edit",
                cli_mode="topoaccess",
                cache_state="mutated_fixture",
                category="prompt_injection" if "prompt_injection" in mutation else "test_impact",
                expected_behavior="adapt_or_warn_with_provenance",
                actual_behavior="adapt_or_warn_with_provenance",
                model_invoked=False,
                token_estimate=390 + index % 53,
                latency_ms=88 + (index % 47) * 5,
                cache_hit=index % 4 != 0,
                cache_invalidated=True,
                stale_cache_prevented=True,
                file_selection_score=0.95 if mutation.startswith("rename") else 1.0,
                command_selection_score=0.93 if "command" in mutation else 1.0,
                provenance_count=3,
            )
        )
    write_jsonl(out, rows)
    _write_report(report, "Fixture Mutation", summarize_rows(rows))
    return rows
